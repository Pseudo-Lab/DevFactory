from pydantic import BaseModel
from typing import List

class ChallengeRequest(BaseModel):
    team_id: int
    my_id: int
    members_ids: List[int]

class AssignedChallenge(BaseModel):
    user_id: int
    assigned_challenge_id: int
    from_user_id: int
    category: str
    answer: str

class ChallengeResponse(BaseModel):
    team_id: int
    my_assigned: AssignedChallenge
from datetime import datetime
from typing import Optional

class GoodsRedeemRequest(BaseModel):
  user_id: int

class GoodsRedeemResponse(BaseModel):
  message: str
  redeemed_at: Optional[datetime] = None

class ChallengeRetryRequest(BaseModel):
  user_id: int

class ChallengeRetryResponse(BaseModel):
  message: str
  retry_count: int
