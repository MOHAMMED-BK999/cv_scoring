from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from app.database import Base
from app.db_types import EmbeddingVector, JsonList
from app.core.embedding_engine import VECTOR_SIZE

class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    required_hard_skills = Column(JsonList(), server_default='[]')
    required_soft_skills = Column(JsonList(), server_default='[]')
    min_experience_years = Column(Integer, default=0)
    required_degree = Column(String(100), nullable=True)
    location = Column(String(255), nullable=True)
    contract_type = Column(String(50), nullable=True)
    embedding_vector = Column(EmbeddingVector(VECTOR_SIZE), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
