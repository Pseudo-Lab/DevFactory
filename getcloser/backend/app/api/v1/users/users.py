from core.database import get_db
from core.dependencies import get_current_user
from fastapi import APIRouter, Depends
from models.users import User
from services.user_service import  get_user, parse_user_id, progress_status
from sqlalchemy.orm import Session
from schemas.user_schema import MeResponse

router = APIRouter()

@router.get("/me")
def get_my_info(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user),
):
  team_id, challenge_id, status = progress_status(
        db=db,
        user_id=current_user["sub"],
    )
  return MeResponse(
        sub=str(current_user["sub"]),
        email=current_user["email"],
        name=current_user["name"],
        exp=current_user["exp"],

        team_id=team_id,
        challenge_id=challenge_id,
        progress_status=status,
    )
  

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
