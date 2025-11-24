from core.database import get_db
from fastapi import APIRouter, Depends
from models.users import User
from services.user_service import auth_user
from sqlalchemy.orm import Session
from schemas.user_schema import UserAuth, UserResponse


router = APIRouter()

# Accept both /auth and /auth/ to avoid redirects (307) when the trailing slash is
# omitted by clients such as the frontend.
@router.post("", response_model=UserResponse)
@router.post("/", response_model=UserResponse, include_in_schema=False)
def auth(user_auth: UserAuth, db: Session = Depends(get_db)):
  token = auth_user(db, user_auth.email)
  return token
