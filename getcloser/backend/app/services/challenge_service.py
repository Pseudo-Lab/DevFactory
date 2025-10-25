import random
from sqlalchemy.orm import Session
from models.challenge_question import ChallengeQuestion
from schemas.challenge_schema import AssignedChallenge

def assign_challenges_logic(members: list, db: Session) -> list:
    team_questions = db.query(ChallengeQuestion).filter(ChallengeQuestion.user_id.in_(members)).all()
    if len(team_questions) < 2:
        raise ValueError("팀원 문제가 충분하지 않습니다.")

    assigned_list = []
    available_ids = members.copy()
    random.shuffle(available_ids)

    for user_id in members:
        possible_ids = [uid for uid in available_ids if uid != user_id]
        if not possible_ids:
            raise ValueError(f"{user_id}에게 할당할 문제 부족")

        assigned_user_id = random.choice(possible_ids)
        assigned_question = random.choice([q for q in team_questions if q.user_id == assigned_user_id])

        available_ids.remove(assigned_user_id)

        assigned_list.append(AssignedChallenge(
            user_id=user_id,
            assigned_challenge_id=assigned_question.id,
            from_user_id=assigned_question.user_id,
            category=assigned_question.category,
            answer=assigned_question.answer
        ))

    return assigned_list
