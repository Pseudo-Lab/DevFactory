from core.security import create_access_token
from exceptions.user_exceptions import UserNotFoundException
from models.users import User
from models.teams import Team, TeamMember, TeamStatus
from models.challenges import UserChallengeStatus
from sqlalchemy.orm import Session
from core.enums import ProgressStatus


def auth_user(db: Session, email: str):
  user = db.query(User).filter(User.email == email).first()
  if not user:
    raise UserNotFoundException(email)
  
  token = create_access_token({
    "sub": str(user.id),
    "email": user.email,
    "name": user.name
    })
  return {"accessToken": token}


def get_user(db: Session, id: int):
  user = db.query(User).filter(User.id == id).first()
  if not user:
    raise UserNotFoundException(id)
  return user


def parse_user_id(tag: str):
  try:
    name, id_str = tag.split("#")
    user_id = int(id_str)
    return {"id": user_id}
  except ValueError:
    return {"error": "올바른 형식의 유저 태그가 아닙니다. 예: 김민준#0001"}


def progress_status(
    db: Session,
    user_id: int,
):
    # 1. 유저 팀 조회
    team_member = (
        db.query(TeamMember)
        .filter(TeamMember.user_id == user_id)
        .first()
    )

    if not team_member:
        return None, None, ProgressStatus.NONE_TEAM

    team = db.query(Team).get(team_member.team_id)

    # 2. 팀 상태
    if team.status == TeamStatus.PENDING:
        return team.id, None, ProgressStatus.TEAM_WAITING

    if team.status == TeamStatus.FAILED:
        return team.id, None, ProgressStatus.FAILED

    # 3. 문제 상태
    ucs = (
        db.query(UserChallengeStatus)
        .filter(UserChallengeStatus.user_id == user_id)
        .first()
    )

    if not ucs:
        return team.id, None, ProgressStatus.CHALLENGE_ASSIGNED

    if ucs.is_redeemed:
        return team.id, ucs.challenge_id, ProgressStatus.REDEEMED

    if ucs.is_correct:
        return team.id, ucs.challenge_id, ProgressStatus.CHALLENGE_SUCCESS

    if ucs.retry_count >= 3:
        return team.id, ucs.challenge_id, ProgressStatus.CHALLENGE_FAILED

    return team.id, ucs.challenge_id, ProgressStatus.CHALLENGE_ASSIGNED
