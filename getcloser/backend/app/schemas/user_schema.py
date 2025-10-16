from pydantic import BaseModel

class UserResponse(BaseModel):
  id: int
  email: str
  name: str
  
  
  class Config:
    orm_mode = True
