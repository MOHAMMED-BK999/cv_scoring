from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

class Language(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=True)
    level = Column(String(50), nullable=True)
