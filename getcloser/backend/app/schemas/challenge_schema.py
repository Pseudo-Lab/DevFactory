from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class ChallengeRequest(BaseModel):
  team_id: int
  my_id: int
  members_ids: List[int]

  class Config:
    json_schema_extra = {
      "example": {
        "team_id": 0,
        "my_id": 1,
        "members_ids": [
          2, 3, 4, 5
        ]
      }
    }

class AssignedChallenge(BaseModel):
  user_id: int
  assigned_challenge_id: int
  from_user_id: int
  category: str
  answer: str

class AnswerSubmitRequest(BaseModel):
  user_id: int
  challenge_id: int
  submitted_answer: str

  class Config:
    json_schema_extra = {
      "example": {
        "user_id": 1,
        "challenge_id": 1,
        "submitted_answer": "LLM"
      }
    }

class AnswerSubmitResponse(BaseModel):
  is_correct: bool

class ChallengeResponse(BaseModel):
  team_id: int
  my_assigned: AssignedChallenge

class GoodsRedeemRequest(BaseModel):
  user_id: int

  class Config:
    json_schema_extra = {
      "example": {
        "user_id": 1
      }
    }

class GoodsRedeemResponse(BaseModel):
  message: str
  redeemed_at: Optional[datetime] = None

class ChallengeRetryRequest(BaseModel):
  user_id: int

  class Config:
    json_schema_extra = {
      "example": {
        "user_id": 1
      }
    }

class ChallengeRetryResponse(BaseModel):
  message: str
  retry_count: int
