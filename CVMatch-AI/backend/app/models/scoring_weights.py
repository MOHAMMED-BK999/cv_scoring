from sqlalchemy import Column, Integer, Float
from app.database import Base

class ScoringWeights(Base):
    __tablename__ = "scoring_weights"

    id = Column(Integer, primary_key=True, index=True)
    skills = Column(Float, nullable=False, default=0.40)
    experience = Column(Float, nullable=False, default=0.30)
    education = Column(Float, nullable=False, default=0.20)
    soft_skills = Column(Float, nullable=False, default=0.10)
