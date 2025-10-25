from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.challenge_schema import ChallengeRequest, ChallengeResponse
from services.challenge_service import assign_challenges_logic
from core.database import get_db

router = APIRouter()

@router.post("/assign-challenges/", response_model=ChallengeResponse)
def assign_challenges(request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        assigned = assign_challenges_logic(request.members_id, db)
        return ChallengeResponse(team_id=request.team_id, assigned=assigned)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
