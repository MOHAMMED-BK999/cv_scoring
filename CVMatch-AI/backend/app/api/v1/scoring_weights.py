from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.scoring_weights import ScoringWeightsCreate, ScoringWeightsResponse
from app.repositories.scoring_weights import scoring_weights_repo

router = APIRouter()

@router.get("/settings/scoring", response_model=ScoringWeightsResponse, tags=["settings"])
async def get_scoring_weights(db: Session = Depends(get_db)):
    """Get current global scoring weights."""
    return scoring_weights_repo.get_weights(db)

@router.post("/settings/scoring", response_model=ScoringWeightsResponse, tags=["settings"])
async def update_scoring_weights(payload: ScoringWeightsCreate, db: Session = Depends(get_db)):
    """Update global scoring weights."""
    return scoring_weights_repo.update_weights(db, payload)
