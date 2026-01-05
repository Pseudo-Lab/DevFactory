
from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from core.database import Base

class UserChallengeStatus(Base):
    __tablename__ = "user_challenge_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, index=True)
    challenge_id = Column(Integer, ForeignKey("challenge_questions.id"), nullable=True)

    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime(timezone=True))
    is_redeemed = Column(Boolean, default=False)
    redeemed_at = Column(DateTime(timezone=True))
    retry_count = Column(Integer, default=0)
    
    challenge = relationship("ChallengeQuestion")