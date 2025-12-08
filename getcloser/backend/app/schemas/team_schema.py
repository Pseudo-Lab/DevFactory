from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class TeamCreateRequest(BaseModel):
    member_ids: List[int] = Field(..., min_items=1, max_items=4, description="팀원 4명의 ID")

class TeamCreateResponse(BaseModel):
    team_id: int
    status: str
    message: str

class TeamStatusResponse(BaseModel):
    team_id: int
    status: str
    members_ready: List[int]
