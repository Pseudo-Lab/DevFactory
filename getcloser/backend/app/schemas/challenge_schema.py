from pydantic import BaseModel
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
