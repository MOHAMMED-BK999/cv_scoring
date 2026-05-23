import json
import os
import re
from typing import Any

import numpy as np

from app.core.embedding_engine import get_embedding
from app.core.extractor_service import CVProfile


def cosine_similarity(a: list[float], b: list[float]) -> float:
    va = np.asarray(a, dtype=np.float32)
    vb = np.asarray(b, dtype=np.float32)
    denom = float(np.linalg.norm(va) * np.linalg.norm(vb))
    if denom == 0:
        return 0.0
    return float(np.dot(va, vb) / denom)


def _keywords(text: str) -> set[str]:
    stopwords = {
        "and",
        "avec",
        "dans",
        "des",
        "for",
        "les",
        "the",
        "une",
        "you",
        "your",
        "will",
        "work",
        "experience",
    }
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", (text or "").lower())
    return {word for word in words if word not in stopwords}


def _percent(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0

    return round(max(0.0, min(100.0, numeric)), 2)


def _normalize_term(term: str) -> str:
    return re.sub(r"\s+", " ", (term or "").strip().lower())


def _term_tokens(term: str) -> set[str]:
    return _keywords(term)


class ScoringService:
    """Notebook phase 4 scoring engine, adapted for the FastAPI upload route."""

    def __init__(self) -> None:
        self.model = os.getenv("OLLAMA_MODEL", "llama3:8b")

    async def score_candidate(
        self,
        cv_profile: CVProfile,
        job_description: str,
        weights: dict[str, float] | None = None,
        required_hard_skills: list[str] | None = None,
        required_soft_skills: list[str] | None = None,
        min_experience_years: float = 0,
        cv_embedding: list[float] | None = None,
        job_embedding: list[float] | None = None,
    ) -> dict[str, Any]:
        weights = weights or {
            "skills": 0.40,
            "experience": 0.30,
            "education": 0.20,
            "soft_skills": 0.10,
        }

        cv_text = self._profile_to_text(cv_profile)
        cv_vector = cv_embedding if cv_embedding is not None else get_embedding(cv_text)
        job_vector = job_embedding if job_embedding is not None else get_embedding(job_description)
        semantic_score = _percent(cosine_similarity(cv_vector, job_vector) * 100)
        fallback = self._heuristic_scores(
            cv_profile,
            job_description,
            semantic_score,
            weights,
            required_hard_skills or [],
            required_soft_skills or [],
            min_experience_years,
        )
        return fallback

    def _profile_to_text(self, cv_profile: CVProfile) -> str:
        skills = ", ".join(cv_profile.flat_skills)
        education = " ".join(f"{item.degree} {item.institution} {item.year}" for item in cv_profile.education)
        experience = " ".join(
            f"{item.role} {item.company} {' '.join(item.description)}" for item in cv_profile.experience
        )
        languages = ", ".join(cv_profile.languages)
        raw_text = getattr(cv_profile, "raw_text", "") or ""
        return f"Skills: {skills}\nExperience: {experience}\nEducation: {education}\nLanguages: {languages}\nSummary: {cv_profile.summary}\nRaw CV: {raw_text}"

    def _heuristic_scores(
        self,
        cv_profile: CVProfile,
        job_description: str,
        semantic_score: float,
        weights: dict[str, float],
        required_hard_skills: list[str],
        required_soft_skills: list[str],
        min_experience_years: float,
    ) -> dict[str, Any]:
        cv_text = self._profile_to_text(cv_profile).lower()
        cv_terms = _keywords(cv_text) | {skill.lower() for skill in cv_profile.flat_skills}

        hard_requirements = [_normalize_term(skill) for skill in required_hard_skills if _normalize_term(skill)]
        if not hard_requirements:
            hard_requirements = sorted(_keywords(job_description))[:25]

        soft_requirements = [_normalize_term(skill) for skill in required_soft_skills if _normalize_term(skill)]

        matched_scores: list[tuple[str, float]] = []
        for skill in hard_requirements:
            tokens = _term_tokens(skill)
            if skill in cv_text:
                matched_scores.append((skill, 1.0))
            elif tokens and tokens.issubset(cv_terms):
                matched_scores.append((skill, 0.85))
            elif tokens:
                overlap = len(tokens & cv_terms) / len(tokens)
                matched_scores.append((skill, overlap * 0.6))
            else:
                matched_scores.append((skill, 0.0))

        matched = [skill for skill, score in matched_scores if score >= 0.5]
        missing = [skill for skill, score in matched_scores if score < 0.5]
        skills_score = _percent((sum(score for _, score in matched_scores) / max(len(matched_scores), 1)) * 100)

        years = float(cv_profile.total_experience_years or 0)
        if min_experience_years and min_experience_years > 0:
            experience_score = _percent((years / min_experience_years) * 100)
        else:
            experience_score = _percent(50 + min(years, 5) * 10 if years else 0)

        education_score = 70.0 if cv_profile.education else 45.0
        if soft_requirements:
            soft_matches = [skill for skill in soft_requirements if skill in cv_text or _term_tokens(skill) & cv_terms]
            soft_score = _percent((len(soft_matches) / max(len(soft_requirements), 1)) * 100)
        else:
            soft_score = _percent(semantic_score * 0.6 + skills_score * 0.4)

        global_score = _percent(
            skills_score * weights.get("skills", 0.40)
            + experience_score * weights.get("experience", 0.30)
            + education_score * weights.get("education", 0.20)
            + soft_score * weights.get("soft_skills", 0.10)
        )

        recommendation = "strong_match" if global_score >= 75 else "maybe" if global_score >= 50 else "not_recommended"
        return {
            "global_score": global_score,
            "semantic_score": semantic_score,
            "skills_score": skills_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "soft_skills_score": soft_score,
            "matched_skills": matched[:20],
            "missing_skills": missing,
            "strengths": matched[:5],
            "gaps": missing[:5],
            "overall_assessment": f"Recommendation: {recommendation}. Matched {len(matched)} relevant terms.",
            "interview_recommendation": recommendation,
        }

    def judge_tied_candidates_with_ollama(
        self,
        candidates: list[dict[str, Any]],
        job_description: str,
        required_hard_skills: list[str],
        required_soft_skills: list[str],
        min_experience_years: float,
        base_score: float,
    ) -> dict[str, Any] | None:
        try:
            import ollama

            prompt = f"""
You are resolving a tie between CVs that received the same automatic score.
Do not create new numeric scores. Judge only who should be ranked first, second, and third inside this tied group, and explain why.
Base your decision on the job description, required hard skills, required soft skills, and minimum experience.

[BASE SCORE]
{base_score}

[JOB DESCRIPTION]
{job_description}

[REQUIRED HARD SKILLS]
{json.dumps(required_hard_skills, ensure_ascii=False)}

[REQUIRED SOFT SKILLS]
{json.dumps(required_soft_skills, ensure_ascii=False)}

[MIN EXPERIENCE YEARS]
{min_experience_years}

[TIED CANDIDATES]
{json.dumps(candidates, ensure_ascii=False, indent=2)}

Return ONLY valid JSON:
{{
  "ranking": [
    {{"candidate_id": 1, "rank": 1, "reason": "why this candidate is first"}},
    {{"candidate_id": 2, "rank": 2, "reason": "why this candidate is second"}}
  ],
  "summary": "short judgement summary"
}}
"""
            response = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                format="json",
                options={"temperature": 0.1},
            )
            return json.loads(response["message"]["content"])
        except Exception:
            return None


scoring_service = ScoringService()
