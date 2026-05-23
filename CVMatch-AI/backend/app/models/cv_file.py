from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class CVFile(Base):
    __tablename__ = "cv_files"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("job_descriptions.id", ondelete="CASCADE"), nullable=False, index=True)
    original_filename = Column(String(500), nullable=False)
    stored_path = Column(String(1000), nullable=False)
    file_type = Column(String(10)) 
    file_size_bytes = Column(Integer)
    status = Column(String(20), default='uploaded', index=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
