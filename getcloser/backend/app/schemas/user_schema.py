from pydantic import BaseModel, EmailStr

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
  
class Config:
  orm_mode = True
