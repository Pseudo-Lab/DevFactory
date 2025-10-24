from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from models.challenges import UserChallengeStatus

def redeem_goods(db: Session, user_id: int):
    user = db.query(UserChallengeStatus).filter(UserChallengeStatus.user_id == user_id).first()
    if not user or not user.is_correct:
        raise HTTPException(status_code=400, detail="퀴즈를 먼저 완료해야 합니다.")
    if user.is_redeemed:
        raise HTTPException(status_code=400, detail="이미 굿즈를 수령했습니다.")

    now = datetime.utcnow()
    user.is_redeemed = True
    user.redeemed_at = now

    db.commit()
    return {"message": "굿즈 수령 완료", "redeemed_at": now}
