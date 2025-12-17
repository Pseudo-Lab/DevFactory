from core.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True, index=True)
  email = Column(String, nullable=False, unique=True)
  name = Column(String, nullable=False)
  linkedin_url = Column(String, nullable=False)
  github_url = Column(String, nullable=True)
