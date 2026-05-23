from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import JobDescription
from app.core.embedding_engine import get_embedding
from app.core.job_text import build_job_text

router = APIRouter()

class JobCreate(BaseModel):
    title: str
    description: str
    required_hard_skills: list[str] = []
    required_soft_skills: list[str] = []
    min_experience_years: int = 0
    required_degree: str | None = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    required_hard_skills: list[str] = []
    required_soft_skills: list[str] = []
    min_experience_years: int = 0
    required_degree: str | None = None

    class Config:
        from_attributes = True

@router.post("/jobs", response_model=JobResponse, tags=["jobs"])
async def create_job(payload: JobCreate, db: Session = Depends(get_db)):
    job_text = build_job_text(
        title=payload.title,
        description=payload.description,
        required_hard_skills=payload.required_hard_skills,
        required_soft_skills=payload.required_soft_skills,
        min_experience_years=payload.min_experience_years,
        required_degree=payload.required_degree,
    )
    vector = get_embedding(job_text)
    
    new_job = JobDescription(
        user_id=1,  # Hardcoded temporarily until Auth is integrated
        title=payload.title,
        description=payload.description,
        required_hard_skills=payload.required_hard_skills,
        required_soft_skills=payload.required_soft_skills,
        min_experience_years=payload.min_experience_years,
        required_degree=payload.required_degree,
        embedding_vector=vector
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return new_job

@router.get("/jobs/{job_id}", response_model=JobResponse, tags=["jobs"])
async def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/jobs", response_model=list[JobResponse], tags=["jobs"])
async def get_all_jobs(db: Session = Depends(get_db)):
    return db.query(JobDescription).all()
