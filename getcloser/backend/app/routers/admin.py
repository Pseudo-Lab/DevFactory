from fastapi import APIRouter, HTTPException
from services.db_reset_service import reset_database

admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.post("/reset_db")
def reset_db():
    try:
        reset_database()
        return {"status": "ok", "message": "Database was reset and seeded."}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database reset failed: {exc}")
