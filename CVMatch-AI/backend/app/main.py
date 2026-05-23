import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import health, upload, jobs, scores
from app.database import (
    Base,
    SessionLocal,
    engine,
    ensure_pgvector_extension,
    ensure_vector_indexes,
    is_sqlite,
)
from app.models import User
app = FastAPI(title="AI CV Scoring - Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="")
app.include_router(upload.router, prefix="/api/v1")
app.include_router(jobs.router, prefix="/api/v1")
app.include_router(scores.router, prefix="/api/v1")


def _seed_default_user() -> None:
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        if user:
            return

        db.add(
            User(
                id=1,
                email="local-recruiter@example.com",
                password_hash="local-dev",
                full_name="Local Recruiter",
                role="recruiter",
            )
        )
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def initialize_database() -> None:
    auto_create_tables = os.getenv("AUTO_CREATE_TABLES", "").lower() in {"1", "true", "yes"}
    if not (is_sqlite() or auto_create_tables):
        return

    ensure_pgvector_extension()
    Base.metadata.create_all(bind=engine)
    ensure_vector_indexes()
    _seed_default_user()


@app.get("/", tags=["root"])
async def root() -> dict:
    return {"message": "AI CV Scoring Backend — running"}
