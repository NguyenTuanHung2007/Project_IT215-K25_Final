from datetime import datetime, timezone

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "success": True,
        "status": "ok",
        "timestamp": datetime.now(timezone.utc),
    }
