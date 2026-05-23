from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=True)
    skill_type = Column(String(10), nullable=True)
    proficiency = Column(String(50), nullable=True)
