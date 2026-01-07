from services import team_service
import random
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from models.challenge_question import ChallengeQuestion
from schemas.challenge_schema import AssignedChallenge
from models.challenges import UserChallengeStatus


def assign_challenges_logic(my_id: int, members: list[int], team_id: int, db: Session) -> list:
    # 현재 사용자 retry_count 조회
    status = db.query(UserChallengeStatus).filter(UserChallengeStatus.user_id == my_id).first()

    # status 없으면 생성
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
        team_service.dissolve_team_by_user(db, my_id, team_id)
        raise HTTPException(status_code=500, detail="over retry count")
    
    # 팀원 리스트가 비어있는 경우
    if not members:
        raise ValueError("members 리스트가 비어 있습니다. 팀원 정보가 전달되지 않았습니다.")

    # 팀원들이 만든 문제 조회
    team_questions = db.query(ChallengeQuestion).filter(ChallengeQuestion.user_id.in_(members)).all()
    if not team_questions:
        raise ValueError("배정할 문제가 없습니다.")

    # 셔플 후 1개 선택
    selected_question = random.choice(team_questions)

    # AssignedChallenge로 변환
    assigned_challenge = AssignedChallenge(
        assigned_challenge_id=selected_question.id,
        user_id=selected_question.user_id,    # 문제 출제자
        category=selected_question.category,
        answer=selected_question.answer,
    )

    # ✅ UserChallengeStatus 업데이트
    user_status = (
        db.query(UserChallengeStatus)
        .filter(UserChallengeStatus.user_id == my_id)
        .first()
    )

    if not user_status:
        raise HTTPException(status_code=404, detail="UserChallengeStatus 없음")

    user_status.challenge_id = selected_question.id
    user_status.submitted_at = None
    user_status.is_correct = False
    user_status.is_redeemed = False

    db.add(user_status)
    db.commit()
    
    return assigned_challenge
    
    
def submit_challenges_logic(my_id: str, challenge_id: int, submitted_answer: str, db: Session) -> bool:
    # # 1. 사용자가 푼 문제 찾기
    # challenge = db.query(ChallengeQuestion).filter(
    #     ChallengeQuestion.user_id == user_id,
    #     ChallengeQuestion.id == challenge_id
    # ).first()

    # if not challenge:
    #     raise ValueError("해당 사용자의 할당된 문제가 없습니다.")

    # 2. 원본 문제에서 정답 확인
    question = db.query(ChallengeQuestion).filter(
        ChallengeQuestion.id == challenge_id
    ).first()

    if not question:
        raise ValueError("문제 정보를 찾을 수 없습니다.")

    # 3. 정답 판별
    answer_keyword = max(question.answer.lower().split(), key=len)
    submitted = submitted_answer.strip().lower()
    is_correct = answer_keyword in submitted

    # 4. UserChallengeStatus 조회 또는 생성
    status = db.query(UserChallengeStatus).filter(
        UserChallengeStatus.user_id == my_id,
        UserChallengeStatus.challenge_id == challenge_id
    ).first()

    if not status:
        status = UserChallengeStatus(
            user_id=my_id,
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
