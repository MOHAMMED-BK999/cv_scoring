import os
import uuid
import logging
from pathlib import Path
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends, Form
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CVFile, CandidateProfile, JobDescription, ScoringResult, Education, Experience

# === Services Modernes 2026 ===
from app.core.cv_parser import CVParser
from app.core.extractor_service import extractor_service, CVProfile
from app.core.embedding_engine import embedding_service
from app.core.job_text import build_job_text
from app.core.scoring_service import scoring_service

logger = logging.getLogger(__name__)

router = APIRouter()

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "./data/uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/octet-stream",
}

# Initialisation des services
cv_parser = CVParser()


def _normalize_weights(
    skills: float,
    experience: float,
    education: float,
    soft_skills: float,
) -> dict[str, float]:
    weights = {
        "skills": skills,
        "experience": experience,
        "education": education,
        "soft_skills": soft_skills,
    }
    if any(value > 1 for value in weights.values()):
        weights = {key: value / 100 for key, value in weights.items()}

    total = sum(weights.values())
    if total <= 0:
        return {
            "skills": 0.40,
            "experience": 0.30,
            "education": 0.20,
            "soft_skills": 0.10,
        }

    return {key: value / total for key, value in weights.items()}


@router.post("/jobs/{job_id}/cvs/upload", tags=["cv"])
async def upload_cv(
    job_id: int, 
    file: UploadFile = File(...), 
    weight_skills: float = Form(0.40),
    weight_experience: float = Form(0.30),
    weight_education: float = Form(0.20),
    weight_soft_skills: float = Form(0.10),
    db: Session = Depends(get_db)
):
    """
    Endpoint moderne d'upload et analyse de CV (Pipeline 2026)
    """
    # 1. Vérification du Job
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # 2. Vérification du type de fichier
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS or file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400, 
            detail="Unsupported file type. Only PDF and DOCX are allowed."
        )

    # 3. Lecture et sauvegarde du fichier
    file_bytes = await file.read()
    cv_uuid = str(uuid.uuid4())
    out_path = UPLOAD_DIR / f"{cv_uuid}{ext}"

    try:
        with out_path.open("wb") as f:
            f.write(file_bytes)

        logger.info(f"CV uploaded: {file.filename} → {out_path}")

        # ====================== PIPELINE COMPLET 2026 ======================
        
        # Parsing avec Docling 2.x
        raw_markdown = cv_parser.parse_cv(file_bytes, file.filename)

        # Extraction structurée (Ollama/Pydantic)
        cv_profile: CVProfile = await extractor_service.extract_cv(raw_markdown)

        # Embedding: create dense vector from structured profile JSON (step 2).
        dense_vector = embedding_service.get_embedding_from_profile(cv_profile)

        # ====================== SAUVEGARDE EN BASE ======================
        
        # CV File
        db_cv = CVFile(
            job_id=job.id,
            original_filename=file.filename,
            stored_path=str(out_path),
            file_type="pdf" if ext == ".pdf" else "docx",
            file_size_bytes=len(file_bytes),

            status="processing"
        )
        db.add(db_cv)
        db.flush()
        db.refresh(db_cv)

        # Candidate Profile
        profile = CandidateProfile(
            cv_file_id=db_cv.id,
            full_name=cv_profile.full_name,
            email=cv_profile.email,
            phone=cv_profile.phone,
            location=cv_profile.location,
            total_experience_years=getattr(cv_profile, 'total_experience_years', 0.0),
            summary_text=cv_profile.summary[:1000] if cv_profile.summary else "",
            raw_text=raw_markdown,
            embedding_vector=dense_vector
        )
        db.add(profile)
        db.flush()
        db.refresh(profile)

        # Save extracted Education details
        for edu in cv_profile.education:
            try:
                year_val = None
                if edu.year:
                    digits = "".join(c for c in str(edu.year) if c.isdigit())
                    if digits:
                        year_val = int(digits[:4])
                db_edu = Education(
                    profile_id=profile.id,
                    degree=edu.degree,
                    institution=edu.institution,
                    graduation_year=year_val
                )
                db.add(db_edu)
            except Exception as e:
                logger.warning(f"Error saving education record: {e}")

        # Save extracted Experience details
        for exp in cv_profile.experience:
            try:
                db_exp = Experience(
                    profile_id=profile.id,
                    job_title=exp.role,
                    company=exp.company,
                    description="\n".join(exp.description) if isinstance(exp.description, list) else str(exp.description)
                )
                db.add(db_exp)
            except Exception as e:
                logger.warning(f"Error saving experience record: {e}")
        db.flush()

        # ====================== SCORING ======================
        weights = _normalize_weights(
            weight_skills,
            weight_experience,
            weight_education,
            weight_soft_skills,
        )
        job_text = build_job_text(
            title=job.title,
            description=job.description,
            required_hard_skills=job.required_hard_skills or [],
            required_soft_skills=job.required_soft_skills or [],
            min_experience_years=job.min_experience_years or 0,
            required_degree=job.required_degree,
        )
        score_result = await scoring_service.score_candidate(
            cv_profile,
            job_text,
            weights,
            required_hard_skills=job.required_hard_skills or [],
            required_soft_skills=job.required_soft_skills or [],
            min_experience_years=job.min_experience_years or 0,
            required_degree=job.required_degree,
            cv_embedding=dense_vector,
            job_embedding=job.embedding_vector,
        )

        # Scoring Result
        scoring = ScoringResult(
            candidate_profile_id=profile.id,
            job_id=job.id,
            global_score=score_result["global_score"],
            semantic_score=score_result.get("semantic_score", 0),
            skills_score=score_result.get("skills_score", 0),
            experience_score=score_result.get("experience_score", 0),
            education_score=score_result.get("education_score", 0),
            explanation=score_result.get("overall_assessment", ""),
            matched_skills=score_result.get("matched_skills", []),
            missing_skills=score_result.get("missing_skills", []),
            # Tu peux ajouter plus de champs selon ton modèle ScoringResult
        )
        db.add(scoring)

        # Mise à jour du statut
        db_cv.status = "scored"
        db.commit()

        logger.info(f"CV {db_cv.id} processed successfully with score: {score_result['global_score']}")

        return {
            "message": "CV processed successfully",
            "cv_id": db_cv.id,
            "candidate_name": cv_profile.full_name,
            "score": score_result["global_score"],
            "global_score": score_result["global_score"],
            "recommendation": score_result.get("interview_recommendation", "maybe")
        }

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing CV {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
