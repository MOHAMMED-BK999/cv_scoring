from fastapi import APIRouter

from app.core.embedding_engine import embedding_service

router = APIRouter()


@router.get("/health", tags=["health"])
async def health() -> dict:
    return {
        "status": "ok",
        "ai_model": embedding_service.model_name
    }


@router.get("/ready", tags=["health"])
async def ready() -> dict:
    # In a full app you'd check DB, Redis, Qdrant etc. Here we return ready.
    return {"ready": True}
