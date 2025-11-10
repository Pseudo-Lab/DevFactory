from core.security import create_access_token
from exceptions.user_exceptions import UserNotFoundException
from models.users import User
from sqlalchemy.orm import Session


def auth_user(db: Session, email: str):
  user = db.query(User).filter(User.email == email).first()
  if not user:
    raise UserNotFoundException(email)
  
  token = create_access_token({
    "sub": str(user.id),
    "email": user.email,
    "name": user.name
    })
  return {"accessToken": token}


def get_user(db: Session, id: int):
  user = db.query(User).filter(User.id == id).first()
  if not user:
    raise UserNotFoundException(id)
  return user


def parse_user_id(tag: str):
  try:
    name, id_str = tag.split("#")
    user_id = int(id_str)
    return {"id": user_id}
  except ValueError:
    return {"error": "올바른 형식의 유저 태그가 아닙니다. 예: 김민준#0001"}
