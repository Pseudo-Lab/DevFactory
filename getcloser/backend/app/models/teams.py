from core.database import Base
from sqlalchemy import Column, Integer, Boolean, UniqueConstraint, Enum, DateTime, ForeignKey, String
import enum
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship

class TeamStatus(str, enum.Enum):
  PENDING = "PENDING"
  ACTIVE = "ACTIVE"
  CANCELLED = "CANCELLED"
  FAILED = "FAILED"
  

class Team(Base):
  __tablename__ = "teams"
  
  id = Column(Integer, primary_key=True, index=True)
  group_hash = Column(String, index=True)
  status = Column(Enum(TeamStatus), nullable=False, default=TeamStatus.PENDING)
  created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

  members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
  

class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    confirmed = Column(Boolean, default=False)

    team = relationship("Team", back_populates="members")

    __table_args__ = (
        UniqueConstraint("team_id", "user_id", name="u_team_user"),
    )
