from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.challenge_schema import GoodsRedeemRequest, GoodsRedeemResponse
from services.challenge_service import redeem_goods

router = APIRouter()

@router.post("/redeem", response_model=GoodsRedeemResponse)
def redeem_goods_controller(request: GoodsRedeemRequest, db: Session = Depends(get_db)):
    return redeem_goods(db, request.user_id)
