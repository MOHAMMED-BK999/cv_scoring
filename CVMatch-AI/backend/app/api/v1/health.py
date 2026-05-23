from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["health"])
async def health() -> dict:
    return {
        "status": "ok",
        "ai_model": "paraphrase-multilingual-MiniLM-L12-v2"
    }


@router.get("/ready", tags=["health"])
async def ready() -> dict:
    # In a full app you'd check DB, Redis, Qdrant etc. Here we return ready.
    return {"ready": True}
