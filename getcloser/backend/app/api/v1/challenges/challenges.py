from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.challenge_schema import ChallengeRequest, ChallengeResponse, ChallengeRetryRequest, ChallengeRetryResponse, GoodsRedeemRequest, GoodsRedeemResponse
from services.challenge_service import assign_challenges_logic, redeem_goods, retry_challenge

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
