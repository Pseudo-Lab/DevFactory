from core.database import Base
from sqlalchemy import Column, Integer, Boolean, UniqueConstraint


class Team(Base):
  __tablename__ = "teams"
  
  id = Column(Integer, primary_key=True, index=True)
  team_id = Column(Integer, index=True)
  user_id = Column(Integer, index=True)
  is_active = Column(Boolean, default=True)

  __table_args__ = (
        UniqueConstraint('team_id', 'user_id', name='_team_user_uc'),
    )
