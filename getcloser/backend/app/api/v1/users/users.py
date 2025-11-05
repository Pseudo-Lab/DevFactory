from core.database import get_db
from fastapi import APIRouter, Depends
from services.user_service import auth_user, get_user, parse_user_id
from sqlalchemy.orm import Session
from schemas.user_schema import UserAuth, UserResponse

router = APIRouter()

@router.post('/auth', response_model=UserResponse)
def auth(user_auth: UserAuth, db: Session = Depends(get_db)):
  user = auth_user(db, user_auth.email)
  return user


@router.get("/{id}")
def get_user_name(id: int, db: Session = Depends(get_db)):
  user = get_user(db, id)
  return {"data": f"{user.name}#{str(user.id).zfill(4)}"}


@router.get("/user_id/{tag}")
def get_user_id(tag: str):
    """
    '이름#0001' 형식의 문자열을 받아서 ID(int)로 변환합니다.
    """
    response = parse_user_id(tag)
    return response