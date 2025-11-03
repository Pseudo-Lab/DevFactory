from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.challenge_schema import ChallengeRequest, ChallengeResponse
from services.challenge_service import assign_challenges_logic
from services.user_service import parse_user_id
from core.database import get_db

router = APIRouter()

@router.post("/assign-challenges", response_model=ChallengeResponse)
def assign_challenges(request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        # my_id = parse_user_id(request.my_id).get("id")
        # if not my_id:
        #     raise HTTPException(status_code=400, detail="올바른 형식의 유저 태그가 아닙니다. 예: 김민준#0001")
        
        # members_ids = [request.my_id]  # 팀원에 자기 자신 포함
        # for tag in request.members_ids:
        #     parsed = parse_user_id(tag)
        #     if "error" in parsed:
        #         raise HTTPException(status_code=400, detail=parsed["error"])
        #     members_ids.append(parsed["id"])

        members_ids = [request.my_id] + request.members_ids
        assigned = assign_challenges_logic(request.my_id, members_ids, db)
        return ChallengeResponse(team_id=request.team_id, my_assigned=assigned)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
