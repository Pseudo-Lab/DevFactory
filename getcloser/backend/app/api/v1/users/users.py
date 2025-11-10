from core.database import get_db
from core.dependencies import get_current_user
from fastapi import APIRouter, Depends
from models.users import User
from services.user_service import  get_user, parse_user_id
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/me")
def get_my_info(
  current_user: User = Depends(get_current_user),
):
  return current_user
  

@router.get("/{id}")
def get_user_name(
  id: int,
  db: Session = Depends(get_db)
  ):
  user = get_user(db, id)
  return {"data": f"{user.name}#{str(user.id).zfill(4)}"}


@router.get("/user_id/{tag}")
def get_user_id(tag: str):
    """
    '이름#0001' 형식의 문자열을 받아서 ID(int)로 변환합니다.
    """
    response = parse_user_id(tag)
    return response
