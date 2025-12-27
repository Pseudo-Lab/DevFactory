from services import team_service
import random
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from models.challenge_question import ChallengeQuestion
from schemas.challenge_schema import AssignedChallenge
from models.challenges import UserChallengeStatus


def assign_challenges_logic(my_id: str, members: list, db: Session) -> list:
    # 현재 사용자 retry_count 조회
    status = db.query(UserChallengeStatus).filter(UserChallengeStatus.user_id == my_id).first()

    # ✅ 없으면 생성
    if not status:
        status = UserChallengeStatus(
            user_id=my_id,
            retry_count=0,
            is_correct=False,
            is_redeemed=False
        )
        db.add(status)
        db.commit()
        db.refresh(status)

    # retry_count 검사
    if status.retry_count >= 2:
        return {"message": "retry_count가 2 이상입니다. 팀을 다시 구성해주세요."}
    
    team_questions = db.query(ChallengeQuestion).filter(ChallengeQuestion.user_id.in_(members)).all()
    if len(team_questions) < len(members):
        raise ValueError("팀원 문제가 충분하지 않습니다.")

    assigned_list = []
    available_ids = members.copy()
    random.shuffle(available_ids)

    members = list(set(members))
    for user_id in members:
        possible_ids = [uid for uid in available_ids if uid != user_id]
        if not possible_ids:
            raise ValueError(f"{user_id}에게 할당할 문제 부족")

        assigned_user_id = random.choice(possible_ids)
        assigned_question = random.choice([q for q in team_questions if q.user_id == assigned_user_id])
        
        available_ids.remove(assigned_user_id)

        # ✅ UserChallengeStatus 업데이트
        user_status = (
            db.query(UserChallengeStatus)
            .filter(UserChallengeStatus.user_id == user_id)
            .first()
        )

        if not user_status:
            raise HTTPException(status_code=404, detail="UserChallengeStatus 없음")

        user_status.challenge_id = assigned_question.id
        user_status.submitted_at = None
        user_status.is_correct = False
        user_status.is_redeemed = False

        db.add(user_status)
        
        assigned_list.append(AssignedChallenge(
            user_id=user_id,
            assigned_challenge_id=assigned_question.id,
            from_user_id=assigned_question.user_id,
            category=assigned_question.category,
            answer=assigned_question.answer
        ))

        db.commit()

    return assigned_list[0]


def submit_challenges_logic(user_id: str, challenge_id: int, submitted_answer: str, db: Session) -> bool:
    # 1. 사용자가 푼 문제 찾기
    challenge = db.query(ChallengeQuestion).filter(
        ChallengeQuestion.user_id == user_id,
        ChallengeQuestion.id == challenge_id
    ).first()

    if not challenge:
        raise ValueError("해당 사용자의 할당된 문제가 없습니다.")

    # 2. 원본 문제에서 정답 확인
    question = db.query(ChallengeQuestion).filter(
        ChallengeQuestion.id == challenge.id
    ).first()

    if not question:
        raise ValueError("문제 정보를 찾을 수 없습니다.")

    # 3. 정답 판별
    is_correct = (submitted_answer.strip().lower() == question.answer.strip().lower())

    # 4. UserChallengeStatus 조회 또는 생성
    status = db.query(UserChallengeStatus).filter(
        UserChallengeStatus.user_id == user_id,
        UserChallengeStatus.challenge_id == challenge_id
    ).first()

    if not status:
        status = UserChallengeStatus(
            user_id=user_id,
            challenge_id=challenge_id,
            retry_count=0
        )
        db.add(status)

    # 5. 결과 저장
    status.is_correct = is_correct
    status.submitted_at = datetime.utcnow()

    if not is_correct:
        status.retry_count += 1

    db.commit()

    # 6. 결과 반환
    return is_correct

   
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
