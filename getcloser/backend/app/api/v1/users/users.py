from core.database import get_db
from fastapi import APIRouter, Depends
from services.user_service import auth_user
from sqlalchemy.orm import Session
from schemas.user_schema import UserAuth, UserResponse

router = APIRouter()

@router.post('/auth', response_model=UserResponse)
def auth(user_auth: UserAuth, db: Session = Depends(get_db)):
  user = auth_user(db, user_auth.email)
  return user
