from pydantic import BaseModel
from typing import List

class ChallengeRequest(BaseModel):
    team_id: int
    members_id: List[int]

class AssignedChallenge(BaseModel):
    user_id: int
    assigned_challenge_id: int
    from_user_id: int
    category: str
    answer: str

class ChallengeResponse(BaseModel):
    team_id: int
    assigned: List[AssignedChallenge]
