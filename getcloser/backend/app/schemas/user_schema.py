from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
  email: EmailStr

class UserResponse(BaseModel):
  accessToken: str
  
class Config:
  orm_mode = True
