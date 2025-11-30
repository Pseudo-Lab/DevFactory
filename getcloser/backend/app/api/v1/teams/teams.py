from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.team_schema import TeamCreateRequest, TeamCreateResponse, TeamStatusResponse
from services.team_service import create_team
from core.dependencies import get_current_user
from core.websocket import notify_invitation

router = APIRouter()

@router.post("/create", response_model=TeamCreateResponse)
async def create_team_route(req: TeamCreateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    res = create_team(db, int(current_user["sub"]), req.member_ids)
    return TeamCreateResponse(**res)

# @router.post("/{team_id}/confirm")
# def confirm_route(team_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
#     return confirm_membership(db, team_id, current_user["sub"])

@router.post("/{team_id}/cancel")
def cancel_route(team_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return cancel_team(db, team_id, current_user["sub"])

@router.get("/{team_id}/status", response_model=TeamStatusResponse)
def status_route(team_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    res = get_team_status(db, team_id, current_user["sub"])
    return TeamStatusResponse(**res)
