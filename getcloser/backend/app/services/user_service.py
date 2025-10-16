from exceptions.user_exceptions import UserNotFoundException
from models.users import User
from sqlalchemy.orm import Session


def auth_user(db: Session, email: str):
  user = db.query(User).filter(User.email == email).first()
  if not user:
    raise UserNotFoundException(email)
  return user
