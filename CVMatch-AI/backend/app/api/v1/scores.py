from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ScoringResult, CandidateProfile, CVFile, Education, Experience

router = APIRouter()


@router.get("/jobs/{job_id}/scores", tags=["scores"])
async def get_job_rankings(job_id: int, db: Session = Depends(get_db)):
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
            "skills_score": float(score.skills_score) if score.skills_score else 0.0,
            "experience_score": float(score.experience_score) if score.experience_score else 0.0,
            "education_score": float(score.education_score) if score.education_score else 0.0,
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

    educations = db.query(Education).filter(Education.profile_id == profile.id).all()
    experiences = db.query(Experience).filter(Experience.profile_id == profile.id).all()

    return {
        "candidate_id": profile.id,
        "full_name": profile.full_name,
        "email": profile.email,
        "phone": profile.phone,
        "location": profile.location,
        "global_score": float(scoring.global_score) if scoring.global_score else 0.0,
        "semantic_score": float(scoring.semantic_score) if scoring.semantic_score else 0.0,
        "skills_score": float(scoring.skills_score) if scoring.skills_score else 0.0,
        "experience_score": float(scoring.experience_score) if scoring.experience_score else 0.0,
        "education_score": float(scoring.education_score) if scoring.education_score else 0.0,
        "explanation": scoring.explanation,
        "matched_skills": scoring.matched_skills or [],
        "missing_skills": scoring.missing_skills or [],
        "educations": [
            {
                "degree": edu.degree or "",
                "school": edu.institution or "",
                "year": str(edu.graduation_year or "")
            } for edu in educations
        ],
        "experiences": [
            {
                "title": exp.job_title or "",
                "company": exp.company or "",
                "duration": f"{exp.start_date or ''} - {exp.end_date or ''}".strip(" -") or "N/A"
            } for exp in experiences
        ]
    }
