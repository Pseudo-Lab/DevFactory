from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from ..database import get_db

test_router = APIRouter(prefix="/test", tags=["test"])

@test_router.get("/ping_db")
def ping_db(db=Depends(get_db)):
    try:
        # 단순 쿼리 실행 (PostgreSQL 연결 확인)
        db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "PostgreSQL 연결 성공"}
    except SQLAlchemyError as e:
        return {"status": "error", "message": str(e)}