from services import team_service
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

def retry_challenge(db: Session, user_id: int):
  user_status = db.query(UserChallengeStatus).filter(UserChallengeStatus.user_id == user_id).first()
  
  if not user_status:
    raise HTTPException(status=404, detail="User not found")
  if user_status.is_correct:
    raise HTTPException(status_code=400, detail="Already solved correctly")
  
  if user_status.retry_count == 0:
    user_status.retry_count += 1
    db.commit()
    return {
      "message": "Retry granted",
      "retry_count": user_status.retry_count
    }
  elif user_status.retry_count >= 1:
    team_service.dissolve_team_by_user(db, user_id)
    return {
      "message": "Team dissolved due to repeated failure",
      "retry_count": user_status.retry_count
    }
