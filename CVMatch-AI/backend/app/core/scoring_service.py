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


def _percent(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return 0.0

    return round(max(0.0, min(100.0, numeric)), 2)


def _normalize(text: str) -> str:
    """Lowercase and strip accents for fuzzy matching."""
    return re.sub(r"[^a-z0-9+#. ]", "", text.lower().strip())


def _skill_matches(
    cv_skills: list[str],
    required: list[str],
) -> tuple[list[str], list[str]]:
    """Return (matched, missing) skill lists using fuzzy substring matching."""
    if not required:
        return [], []

    cv_normalized = [_normalize(s) for s in cv_skills]
    cv_text_blob = " ".join(cv_normalized)

    matched: list[str] = []
    missing: list[str] = []

    for req in required:
        req_norm = _normalize(req)
        found = False
        for cv_s in cv_normalized:
            if req_norm in cv_s or cv_s in req_norm:
                found = True
                break
        if not found and req_norm in cv_text_blob:
            found = True
        if found:
            matched.append(req)
        else:
            missing.append(req)

    return matched, missing


def _compute_skills_score(
    cv_profile: CVProfile,
    required_hard_skills: list[str],
) -> tuple[float, list[str], list[str]]:
    """Compute a 0-100 score for hard/technical skills matching."""
    if not required_hard_skills:
        return 100.0, [], []

    cv_skills = cv_profile.flat_skills
    # Also check raw_text for skill keywords
    raw_lower = (getattr(cv_profile, "raw_text", "") or "").lower()
    summary_lower = (cv_profile.summary or "").lower()
    combined_text = raw_lower + " " + summary_lower

    matched: list[str] = []
    missing: list[str] = []

    for req in required_hard_skills:
        req_norm = _normalize(req)
        found = False
        # Check in extracted skills
        for cv_s in cv_skills:
            cv_s_norm = _normalize(cv_s)
            if req_norm in cv_s_norm or cv_s_norm in req_norm:
                found = True
                break
        # Fallback: check in raw text
        if not found and req_norm in combined_text:
            found = True
        if found:
            matched.append(req)
        else:
            missing.append(req)

    score = (len(matched) / len(required_hard_skills)) * 100.0
    return round(score, 2), matched, missing


def _compute_soft_skills_score(
    cv_profile: CVProfile,
    required_soft_skills: list[str],
) -> float:
    """Compute a 0-100 score for soft skills matching."""
    if not required_soft_skills:
        return 100.0

    cv_skills = cv_profile.flat_skills
    raw_lower = (getattr(cv_profile, "raw_text", "") or "").lower()
    summary_lower = (cv_profile.summary or "").lower()
    combined = " ".join([_normalize(s) for s in cv_skills]) + " " + raw_lower + " " + summary_lower

    found_count = 0
    for req in required_soft_skills:
        req_norm = _normalize(req)
        if req_norm in combined:
            found_count += 1

    return round((found_count / len(required_soft_skills)) * 100.0, 2)


def _compute_experience_score(
    cv_profile: CVProfile,
    min_experience_years: float,
) -> float:
    """Compute a 0-100 score for experience match."""
    candidate_years = float(getattr(cv_profile, "total_experience_years", 0) or 0)

    if min_experience_years <= 0:
        # No requirement: give full credit if candidate has any experience
        if candidate_years > 0:
            return 100.0
        # Even with no parsed years, having experience entries counts
        if cv_profile.experience:
            return 75.0
        return 50.0

    ratio = candidate_years / min_experience_years
    if ratio >= 1.0:
        return 100.0
    elif ratio >= 0.75:
        return 85.0
    elif ratio >= 0.5:
        return 65.0
    elif ratio > 0:
        return 40.0
    else:
        # No years parsed but has experience entries
        if cv_profile.experience:
            return 50.0
        return 0.0


def _compute_education_score(
    cv_profile: CVProfile,
    required_degree: str | None,
) -> float:
    """Compute a 0-100 score for education match."""
    if not cv_profile.education:
        return 0.0 if required_degree else 50.0

    if not required_degree:
        return 100.0 if cv_profile.education else 50.0

    # Degree hierarchy for matching
    degree_levels = {
        "bac": 1, "baccalauréat": 1, "baccalaureat": 1, "high school": 1,
        "bts": 2, "dut": 2, "deug": 2, "associate": 2,
        "licence": 3, "bachelor": 3, "bsc": 3, "ba": 3, "license": 3,
        "master": 4, "msc": 4, "ma": 4, "mba": 4, "maîtrise": 4, "maitrise": 4,
        "ingénieur": 4, "ingenieur": 4, "engineer": 4,
        "doctorat": 5, "phd": 5, "doctorate": 5, "docteur": 5,
    }

    def _get_level(text: str) -> int:
        text_lower = text.lower()
        best = 0
        for keyword, level in degree_levels.items():
            if keyword in text_lower and level > best:
                best = level
        return best

    required_level = _get_level(required_degree)
    candidate_level = max((_get_level(edu.degree) for edu in cv_profile.education), default=0)

    if candidate_level == 0 and required_level == 0:
        return 75.0
    if required_level == 0:
        return 100.0
    if candidate_level >= required_level:
        return 100.0
    if candidate_level == required_level - 1:
        return 70.0
    if candidate_level > 0:
        return 40.0
    return 10.0


class ScoringService:
    """Score candidates using cosine similarity + sub-score analysis."""

    async def score_candidate(
        self,
        cv_profile: CVProfile,
        job_description: str,
        weights: dict[str, float] | None = None,
        required_hard_skills: list[str] | None = None,
        required_soft_skills: list[str] | None = None,
        min_experience_years: float = 0,
        required_degree: str | None = None,
        cv_embedding: list[float] | None = None,
        job_embedding: list[float] | None = None,
    ) -> dict[str, Any]:
        # --- Semantic similarity ---
        cv_text = self._profile_to_text(cv_profile)
        cv_vector = cv_embedding if cv_embedding is not None else get_embedding(cv_text)
        job_vector = job_embedding if job_embedding is not None else get_embedding(job_description)
        semantic_score = _percent(cosine_similarity(cv_vector, job_vector) * 100)

        # --- Sub-scores ---
        skills_score, matched_skills, missing_skills = _compute_skills_score(
            cv_profile, required_hard_skills or []
        )
        soft_skills_score = _compute_soft_skills_score(
            cv_profile, required_soft_skills or []
        )
        experience_score = _compute_experience_score(
            cv_profile, min_experience_years
        )
        education_score = _compute_education_score(
            cv_profile, required_degree
        )

        # --- Weighted global score ---
        if weights is None:
            # Try to fetch from DB
            try:
                from app.database import SessionLocal
                from app.repositories.scoring_weights import scoring_weights_repo
                db = SessionLocal()
                try:
                    db_weights = scoring_weights_repo.get_weights(db)
                    weights = {
                        "skills": db_weights.skills,
                        "experience": db_weights.experience,
                        "education": db_weights.education,
                        "soft_skills": db_weights.soft_skills,
                    }
                finally:
                    db.close()
            except Exception:
                weights = {
                    "skills": 0.40,
                    "experience": 0.30,
                    "education": 0.20,
                    "soft_skills": 0.10,
                }

        # Blend: 40% semantic + 60% weighted sub-scores
        weighted_sub = (
            weights.get("skills", 0.40) * skills_score
            + weights.get("experience", 0.30) * experience_score
            + weights.get("education", 0.20) * education_score
            + weights.get("soft_skills", 0.10) * soft_skills_score
        )
        global_score = _percent(0.40 * semantic_score + 0.60 * weighted_sub)

        # --- Recommendation ---
        recommendation = (
            "strong_match"
            if global_score >= 70
            else "maybe"
            if global_score >= 45
            else "not_recommended"
        )

        # --- Strengths & Gaps ---
        strengths: list[str] = []
        gaps: list[str] = []

        if skills_score >= 75:
            strengths.append(f"Strong technical skills match ({skills_score:.0f}%)")
        elif skills_score < 50 and (required_hard_skills or []):
            gaps.append(f"Missing key technical skills: {', '.join(missing_skills[:5])}")

        if experience_score >= 75:
            strengths.append(f"Experience meets requirements ({experience_score:.0f}%)")
        elif experience_score < 50:
            gaps.append(f"Experience below requirements ({experience_score:.0f}%)")

        if education_score >= 75:
            strengths.append(f"Education level matches ({education_score:.0f}%)")
        elif education_score < 50:
            gaps.append(f"Education level may not meet requirements ({education_score:.0f}%)")

        if soft_skills_score >= 75:
            strengths.append(f"Good soft skills match ({soft_skills_score:.0f}%)")

        if semantic_score >= 70:
            strengths.append(f"High semantic relevance ({semantic_score:.0f}%)")

        return {
            "global_score": global_score,
            "semantic_score": semantic_score,
            "skills_score": _percent(skills_score),
            "experience_score": _percent(experience_score),
            "education_score": _percent(education_score),
            "soft_skills_score": _percent(soft_skills_score),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "gaps": gaps,
            "overall_assessment": (
                f"Recommendation: {recommendation}. "
                f"Global: {global_score}% | Semantic: {semantic_score}% | "
                f"Skills: {skills_score}% | Experience: {experience_score}% | "
                f"Education: {education_score}% | Soft Skills: {soft_skills_score}%."
            ),
            "interview_recommendation": recommendation,
        }

    def _profile_to_text(self, cv_profile: CVProfile) -> str:
        skills = ", ".join(cv_profile.flat_skills)
        education = " ".join(f"{item.degree} {item.institution} {item.year}" for item in cv_profile.education)
        experience = " ".join(
            f"{item.role} {item.company} {' '.join(item.description)}" for item in cv_profile.experience
        )
        languages = ", ".join(cv_profile.languages)
        raw_text = getattr(cv_profile, "raw_text", "") or ""
        return (
            f"Skills: {skills}\n"
            f"Experience: {experience}\n"
            f"Education: {education}\n"
            f"Languages: {languages}\n"
            f"Summary: {cv_profile.summary}\n"
            f"Raw CV: {raw_text}"
        )


scoring_service = ScoringService()
