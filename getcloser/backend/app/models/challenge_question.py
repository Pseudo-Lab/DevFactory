from core.database import Base
from sqlalchemy import Column, Integer, String

class ChallengeQuestion(Base):
    __tablename__ = 'challenge_questions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    category = Column(String)
    answer = Column(String)
