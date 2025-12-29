from pydantic import BaseModel, EmailStr
from typing import Optional
from core.enums import ProgressStatus

class UserAuth(BaseModel):
  email: EmailStr

  class Config:
    json_schema_extra = {
      "example": {
        "email": "minjun_kim@gmail.com"
      }
    }

class UserResponse(BaseModel):
  accessToken: str

class MeResponse(BaseModel):
    sub: str
    email: str
    name: str
    exp: int

    team_id: Optional[int]
    challenge_id: Optional[int]
    progress_status: ProgressStatus

class Config:
  orm_mode = True
