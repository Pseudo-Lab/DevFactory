from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.team_schema import TeamCreateRequest, TeamCreateResponse, TeamStatusResponse, MemberChallengeResponse
from services.team_service import create_team
from core.dependencies import get_current_user

router = APIRouter()

@router.post("/create", response_model=TeamCreateResponse)
async def create_team_route(req: TeamCreateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    res = create_team(db, int(current_user["sub"]), req.member_ids)
    return TeamCreateResponse(**res)

@router.post("/{team_id}/cancel")
def cancel_route(team_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return cancel_team(db, team_id, current_user["sub"])

@router.get("/{team_id}/status", response_model=TeamStatusResponse)
def status_route(team_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    res = get_team_status(db, team_id, current_user["sub"])
    return TeamStatusResponse(**res)

@router.get("/me")
def get_my_team_info(
  db: Session = Depends(get_db), 
  current_user=Depends(get_current_user)
):
  return get_team_info(db, current_user["sub"])

@router.get("/{team_id}/members/{user_id}/challenge",
            response_model=MemberChallengeResponse)
def get_member_challenge(
    team_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_team_member_challenge(db, current_user["sub"], team_id, user_id)
