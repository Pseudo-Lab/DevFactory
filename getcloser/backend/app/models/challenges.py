
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base

class UserChallengeStatus(Base):
    __tablename__ = "user_challenge_status"
    user_id = Column(Integer, primary_key=True, index=True)
    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True))
    is_redeemed = Column(Boolean, default=False)
    redeemed_at = Column(DateTime(timezone=True))
    retry_count = Column(Integer, default=0)
    