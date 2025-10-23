from sqlalchemy.orm import Session
from models.teams import Team
from schemas.team_schema import TeamCreateRequest, TeamResponse
from fastapi import HTTPException

def create_team(db: Session, req: TeamCreateRequest) -> TeamResponse:
    all_ids = [req.my_id] + req.member_ids

    existing = db.query(Team).filter(Team.user_id.in_(all_ids)).all()
    if existing:
        raise HTTPException(status_code=400, detail="Some users are already in a team.")

    last_team = (
        db.query(Team)
        .order_by(Team.team_id.desc())
        .with_for_update()
        .first()
    )

    new_team_id = (last_team.team_id + 1) if last_team else 1

    for uid in all_ids:
        db.add(Team(team_id=new_team_id, user_id=uid))
    
    db.commit()

    return TeamResponse(team_id=new_team_id, members_ids=all_ids)
