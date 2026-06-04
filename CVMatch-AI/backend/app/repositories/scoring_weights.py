from sqlalchemy.orm import Session
from app.models.scoring_weights import ScoringWeights
from app.schemas.scoring_weights import ScoringWeightsCreate

class ScoringWeightsRepository:
    def get_weights(self, db: Session) -> ScoringWeights:
        """Fetch the single global configuration of weights."""
        weights = db.query(ScoringWeights).first()
        if not weights:
            # Create default weights if they don't exist
            weights = ScoringWeights(
                skills=0.40,
                experience=0.30,
                education=0.20,
                soft_skills=0.10
            )
            db.add(weights)
            db.commit()
            db.refresh(weights)
        return weights

    def update_weights(self, db: Session, payload: ScoringWeightsCreate) -> ScoringWeights:
        """Update or create the global weights."""
        weights = db.query(ScoringWeights).first()
        if not weights:
            weights = ScoringWeights(
                skills=payload.skills,
                experience=payload.experience,
                education=payload.education,
                soft_skills=payload.soft_skills
            )
            db.add(weights)
        else:
            weights.skills = payload.skills
            weights.experience = payload.experience
            weights.education = payload.education
            weights.soft_skills = payload.soft_skills

        db.commit()
        db.refresh(weights)
        return weights

scoring_weights_repo = ScoringWeightsRepository()
