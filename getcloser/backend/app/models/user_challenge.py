from core.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class UserChallengeStatus(Base):
    __tablename__ = "user_challenge_status"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenge_questions.id"), nullable=False)
    is_correct = Column(Boolean, default=False)
    submitted_at = Column(DateTime, nullable=True)
    is_redeemed = Column(Boolean, default=False)
    redeemed_at = Column(DateTime, nullable=True)