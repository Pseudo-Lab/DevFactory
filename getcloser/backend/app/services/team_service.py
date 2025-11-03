from sqlalchemy.orm import Session
from models.teams import Team
from schemas.team_schema import TeamCreateRequest, TeamResponse
from fastapi import HTTPException

def create_team(db: Session, req: TeamCreateRequest) -> TeamResponse:
    all_ids = [req.my_id] + req.member_ids

    existing = (
            db.query(Team)
            .filter(Team.user_id.in_(all_ids), Team.is_active == True)
            .all()
        )
   
    if existing:
            active_ids = [e.user_id for e in existing]
            raise HTTPException(
                status_code=400,
                detail=f"Users already in active team: {active_ids}",
            )

    for uid in all_ids:
            prev_teammates = get_prev_team_users(db, uid)
            if any(mid in prev_teammates for mid in all_ids if mid != uid):
                raise HTTPException(
                    status_code=400,
                    detail=f"User {uid} has previously teamed with one of the members.",
                )

    last_team = (
        db.query(Team)
        .order_by(Team.team_id.desc())
        .with_for_update()
        .first()
    )

    new_team_id = (last_team.team_id + 1) if last_team else 1

    for uid in all_ids:
        db.add(Team(team_id=new_team_id, user_id=uid, is_active=True))
    
    db.commit()

    return TeamResponse(team_id=new_team_id, members_ids=all_ids)

def get_prev_team_users(db: Session, user_id: int):
  subquery = db.query(Team.team_id).filter(Team.user_id == user_id).subquery()
  teammates = (
    db.query(Team.user_id)
    .filter(Team.team_id.in_(subquery))
    .distinct()
    .all()
  )
  return {t[0] for t in teammates if t[0] != user_id}

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
