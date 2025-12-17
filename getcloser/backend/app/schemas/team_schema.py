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

class TeamMemberInfo(BaseModel):
    user_id: int
    name: str
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    
class TeamInfoResponse(BaseModel):
    team_id: int
    status: str
    members: List[TeamMemberInfo]
    
class MemberChallengeResponse(BaseModel):
    user_id: int
    question: str
    user_answer: str
    correct_answer: str
    is_correct: bool
