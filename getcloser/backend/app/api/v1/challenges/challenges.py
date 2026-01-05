from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.challenge_schema import ChallengeRequest, ChallengeResponse, ChallengeRetryRequest, ChallengeRetryResponse, GoodsRedeemRequest, GoodsRedeemResponse, AnswerSubmitRequest, AnswerSubmitResponse
from services.challenge_service import assign_challenges_logic, submit_challenges_logic, redeem_goods, retry_challenge

router = APIRouter()

@router.post("/redeem", response_model=GoodsRedeemResponse)
def redeem_goods_controller(request: GoodsRedeemRequest, db: Session = Depends(get_db)):
  return redeem_goods(db, request.user_id)

@router.post("/retry", response_model=ChallengeRetryResponse)
def challenge_retry_controller(request: ChallengeRetryRequest, db: Session = Depends(get_db)):
  return retry_challenge(db, request.user_id)

@router.post("/assign", response_model=ChallengeResponse)
def assign_challenges(request: ChallengeRequest, db: Session = Depends(get_db)):
    try:
        assigned = assign_challenges_logic(request.my_id, request.members_ids, request.team_id, db)
        return ChallengeResponse(team_id=request.team_id, my_assigned=assigned)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/submit", response_model=AnswerSubmitResponse)
def submit_challenges(request: AnswerSubmitRequest, db: Session = Depends(get_db)):
    try:
        is_correct = submit_challenges_logic(request.user_id, request.challenge_id, request.submitted_answer, db)
        return AnswerSubmitResponse(is_correct=is_correct)
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
