from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.team_schema import TeamCreateRequest, TeamResponse
from services.team_service import create_team

router = APIRouter()

@router.post("/create", response_model=TeamResponse)
def create_team_route(req: TeamCreateRequest, db: Session = Depends(get_db)):
    return create_team(db, req)
