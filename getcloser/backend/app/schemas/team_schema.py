from pydantic import BaseModel, Field
from typing import List


class TeamCreateRequest(BaseModel):
    my_id: int
    member_ids: List[int] = Field(..., min_items=4, max_items=4, description="팀원 4명의 ID")

    class Config:
        json_schema_extra = {
            "example": {
                "my_id": 1,
                "member_ids": [2, 3, 4, 5]
            }
    }

class TeamResponse(BaseModel):
    team_id: int
    members_ids: List[int]
