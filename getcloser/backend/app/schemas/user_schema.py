from pydantic import BaseModel, EmailStr

class UserAuth(BaseModel):
  email: EmailStr

class UserResponse(BaseModel):
  id: int
  email: str
  name: str
  
  
  class Config:
    orm_mode = True
