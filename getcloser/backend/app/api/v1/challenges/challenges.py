from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.challenge_schema import ChallengeRetryRequest, ChallengeRetryResponse, GoodsRedeemRequest, GoodsRedeemResponse
from services.challenge_service import redeem_goods, retry_challenge

router = APIRouter()

@router.post("/redeem", response_model=GoodsRedeemResponse)
def redeem_goods_controller(request: GoodsRedeemRequest, db: Session = Depends(get_db)):
  return redeem_goods(db, request.user_id)

@router.post("/retry", response_model=ChallengeRetryResponse)
def challenge_retry_controller(request: ChallengeRetryRequest, db: Session = Depends(get_db)):
  return retry_challenge(db, request.user_id)
