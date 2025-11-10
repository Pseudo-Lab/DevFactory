from models.challenges import UserChallengeStatus
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.teams import Team
from schemas.team_schema import TeamCreateRequest, TeamResponse
from fastapi import HTTPException

def create_team(db: Session, req: TeamCreateRequest) -> TeamResponse:
    all_ids = [req.my_id] + req.member_ids

    records = (
        db.query(Team.user_id, Team.is_active, UserChallengeStatus.is_correct)
        .outerjoin(UserChallengeStatus, Team.user_id == UserChallengeStatus.user_id)
        .filter(Team.user_id.in_(all_ids))
        .all()
    )
    
    active_ids = [r.user_id for r in records if r.is_active]
    corrected_ids = [r.user_id for r in records if r.is_correct]
    
    if active_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Users already in active team: {active_ids}",
        )

    if corrected_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Users already corrected: {corrected_ids}",
        )

    last_team_id = db.query(func.max(Team.team_id)).scalar()
    new_team_id = (last_team_id or 0) + 1

    teams_to_add = [
      {"team_id": new_team_id, "user_id": uid, "is_active": True}
      for uid in all_ids
    ]
    
    db.bulk_insert_mappings(Team, teams_to_add)
    db.commit()

    return TeamResponse(team_id=new_team_id, members_ids=all_ids)

def dissolve_team_by_user(db: Session, user_id: int):
  team_entry = db.query(Team).filter(Team.user_id == user_id, Team.is_active == True).first()
  if not team_entry:
      raise HTTPException(status_code=400, detail="User not in active team")

  team_id = team_entry.team_id
  team_members = db.query(Team).filter(Team.team_id == team_id, Team.is_active == True).all()

  for member in team_members:
      member.is_active = False

  db.commit()
  return {"message": f"Team {team_id} dissolved", "team_id": team_id}
