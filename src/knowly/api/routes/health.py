
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.knowly.db.session import get_db


router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health_check(
    db: AsyncSession = Depends(get_db),
):
    try:
        await db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "service": "Knowly API",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "database": "disconnected",
            },
        )
