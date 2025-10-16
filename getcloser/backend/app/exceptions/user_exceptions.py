from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
  def __init__(self, email: str):
    super().__init__(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail=f"'Not found email::{email}"
    )
