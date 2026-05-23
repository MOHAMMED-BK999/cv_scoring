from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ScoringResult, CandidateProfile, CVFile, JobDescription
from app.core.job_text import build_job_text
from app.core.scoring_service import scoring_service

router = APIRouter()


JUDGEMENT_MARKER = "[Ollama judgement]"


def _extract_tie_rank(explanation: str | None) -> int:
    if not explanation or JUDGEMENT_MARKER not in explanation:
        return 999

    marker_text = explanation.split(JUDGEMENT_MARKER, 1)[1]
    try:
        return int(marker_text.split("Rank ", 1)[1].split("/", 1)[0])
    except (IndexError, ValueError):
        return 999


def _extract_ollama_judgement(explanation: str | None) -> str | None:
    if not explanation or JUDGEMENT_MARKER not in explanation:
        return None

    return explanation.split(JUDGEMENT_MARKER, 1)[1].strip()


def _apply_ollama_tie_breakers(job_id: int, db: Session) -> None:
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        return

    rows = (
        db.query(ScoringResult, CandidateProfile)
        .join(CandidateProfile, ScoringResult.candidate_profile_id == CandidateProfile.id)
        .filter(ScoringResult.job_id == job_id)
        .all()
    )

    tied_by_score: dict[float, list[tuple[ScoringResult, CandidateProfile]]] = {}
    for score, profile in rows:
        rate = round(float(score.global_score or 0), 2)
        tied_by_score.setdefault(rate, []).append((score, profile))

    changed = False
    job_text = build_job_text(
        title=job.title,
        description=job.description,
        required_hard_skills=job.required_hard_skills or [],
        required_soft_skills=job.required_soft_skills or [],
        min_experience_years=job.min_experience_years or 0,
        required_degree=job.required_degree,
    )
    for base_score, tied_rows in tied_by_score.items():
        if len(tied_rows) not in {2, 3}:
            continue

        if all(score.explanation and JUDGEMENT_MARKER in score.explanation for score, _ in tied_rows):
            continue

        candidates = []
        for score, profile in tied_rows:
            candidates.append(
                {
                    "candidate_id": profile.id,
                    "name": profile.full_name or f"Candidate {profile.id}",
                    "summary": profile.summary_text or "",
                    "cv_text": (profile.raw_text or "")[:6000],
                    "automatic_score": base_score,
                    "skills_score": float(score.skills_score or 0),
                    "experience_score": float(score.experience_score or 0),
                    "education_score": float(score.education_score or 0),
                    "semantic_score": float(score.semantic_score or 0),
                }
            )

        judgement = scoring_service.judge_tied_candidates_with_ollama(
            candidates=candidates,
            job_description=job_text,
            required_hard_skills=job.required_hard_skills or [],
            required_soft_skills=job.required_soft_skills or [],
            min_experience_years=job.min_experience_years or 0,
            base_score=base_score,
        )
        if not judgement:
            continue

        by_candidate_id = {
            int(item.get("candidate_id")): item
            for item in judgement.get("ranking", [])
            if item.get("candidate_id") is not None
        }
        group_size = len(tied_rows)
        summary = judgement.get("summary", "Ollama judged this tied group.")

        for score, profile in tied_rows:
            item = by_candidate_id.get(profile.id)
            if not item:
                continue

            rank = int(item.get("rank", group_size))
            reason = item.get("reason", "")
            base_explanation = (score.explanation or "").split(JUDGEMENT_MARKER, 1)[0].strip()
            judgement_text = f"{JUDGEMENT_MARKER} Rank {rank}/{group_size}: {reason} Summary: {summary}"
            score.explanation = f"{base_explanation}\n{judgement_text}".strip()
            changed = True

    if changed:
        db.commit()


@router.get("/jobs/{job_id}/scores", tags=["scores"])
async def get_job_rankings(job_id: int, db: Session = Depends(get_db)):
    _apply_ollama_tie_breakers(job_id, db)

    results = (
        db.query(ScoringResult, CandidateProfile, CVFile)
        .join(CandidateProfile, ScoringResult.candidate_profile_id == CandidateProfile.id)
        .join(CVFile, CandidateProfile.cv_file_id == CVFile.id)
        .filter(ScoringResult.job_id == job_id)
        .all()
    )
    results = sorted(
        results,
        key=lambda row: (
            -(float(row[0].global_score or 0)),
            _extract_tie_rank(row[0].explanation),
            row[1].id,
        ),
    )
    
    response = []
    for score, profile, cv in results:
        response.append({
            "candidate_id": profile.id,
            "cv_id": cv.id,
            "cv_filename": cv.original_filename,
            "email": profile.email,
            "global_score": float(score.global_score) if score.global_score else 0.0,
            "semantic_score": float(score.semantic_score) if score.semantic_score else 0.0,
            "ollama_judgement": _extract_ollama_judgement(score.explanation),
        })
        
    return {"job_id": job_id, "rankings": response}

@router.get("/cvs/{cv_id}/score", tags=["scores"])
async def get_cv_score_detail(cv_id: int, db: Session = Depends(get_db)):
    cv = db.query(CVFile).filter(CVFile.id == cv_id).first()
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
        
    profile = db.query(CandidateProfile).filter(CandidateProfile.cv_file_id == cv_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Candidate profile not generated yet")

    scoring = db.query(ScoringResult).filter(ScoringResult.candidate_profile_id == profile.id).first()
    if not scoring:
        raise HTTPException(status_code=404, detail="Score not found for CV")

    return {
        "candidate_id": profile.id,
        "global_score": float(scoring.global_score) if scoring.global_score else 0.0,
        "semantic_score": float(scoring.semantic_score) if scoring.semantic_score else 0.0,
        "skills_score": float(scoring.skills_score) if scoring.skills_score else 0.0,
        "experience_score": float(scoring.experience_score) if scoring.experience_score else 0.0,
        "education_score": float(scoring.education_score) if scoring.education_score else 0.0,
        "explanation": scoring.explanation,
        "ollama_judgement": _extract_ollama_judgement(scoring.explanation),
        "matched_skills": scoring.matched_skills,
        "missing_skills": scoring.missing_skills
    }
