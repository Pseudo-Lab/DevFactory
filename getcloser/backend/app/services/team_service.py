from models.challenges import UserChallengeStatus
from sqlalchemy import func
from sqlalchemy.orm import Session
from models.teams import Team, TeamMember, TeamStatus
from schemas.team_schema import TeamCreateRequest
from fastapi import HTTPException
from typing import List
import os
from datetime import datetime, timedelta

TEAM_SIZE = int(os.getenv("TEAM_SIZE", "0"))
PENDING_TIMEOUT_MINUTES = int(os.getenv("PENDING_TIMEOUT_MINUTES", "0"))

def _now():
    return datetime.utcnow()

def create_team(db: Session, my_id: int, member_ids: List[int]):
    all_ids = sorted([my_id] + member_ids)

    if len(all_ids) != TEAM_SIZE:
        raise HTTPException(status_code=400, detail="Team must have exactly 5 members (you + 4).")
    if len(set(all_ids)) != TEAM_SIZE:
        raise HTTPException(status_code=400, detail="Duplicate user IDs in request.")
      
    corrected = db.query(UserChallengeStatus.user_id).filter(
          UserChallengeStatus.user_id.in_(all_ids),
          UserChallengeStatus.is_correct == True
    ).all()

    if corrected:
        corrected_ids = [r[0] for r in corrected]
        raise HTTPException(status_code=400, detail=f"Users already corrected: {corrected_ids}")
 
    blocking_users = (
        db.query(TeamMember.user_id)
        .join(Team)
        .filter(
            TeamMember.user_id.in_(all_ids),
            Team.status == TeamStatus.ACTIVE
        )
        .all()
    )
    if blocking_users:
        raise HTTPException(status_code=400,
                            detail=f"Users already in another team: {[u[0] for u in blocking_users]}")
 
    group_hash = "-".join(map(str, all_ids))
    
    team = (
        db.query(Team)
        .filter(Team.group_hash == group_hash,
                Team.status.in_([TeamStatus.PENDING, TeamStatus.ACTIVE]))
        .first()
    )
    
    target_team = None
    
    if team and team.status == TeamStatus.PENDING:
        if _now() - team.created_at.replace(tzinfo=None) > timedelta(minutes=PENDING_TIMEOUT_MINUTES):
            team.status = TeamStatus.CANCELLED
            db.commit()
        else:
            my_member = (
                db.query(TeamMember)
                .filter(TeamMember.team_id == team.id, TeamMember.user_id == my_id)
                .first()
            )
            if my_member:
                my_member.confirmed = True
            
            db.flush()

            ready_count = (
                db.query(TeamMember)
                .filter(TeamMember.team_id == team.id, TeamMember.confirmed == True)
                .count()
            )

            if ready_count == TEAM_SIZE:
                team.status = TeamStatus.ACTIVE
                db.commit()
                return {"status": "ACTIVE", "team_id": team.id, "message": "Team matched"}

            db.commit()
            return {"status": "PENDING", "team_id": team.id, "message": "Joined pending team request"}
    
    if team and team.status == TeamStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="This team is already active.")
        
    team = Team(group_hash=group_hash, status=TeamStatus.PENDING)
    db.add(team)
    db.flush()

    members = [
        TeamMember(team_id=team.id, user_id=uid, confirmed=(uid == my_id))
        for uid in all_ids
    ]
    db.bulk_save_objects(members)
    db.commit()

    return {"status": "PENDING", "team_id": team.id, "message": "New team request created"}

def cancel_team(db: Session, team_id: int, user_id: int):
  team_entry = (
        db.query(Team)
        .join(TeamMember)
        .filter(
            TeamMember.user_id == user_id, 
            Team.status == TeamStatus.PENDING
        ).first()
    )
    
  if team_entry:
      team_entry.status = TeamStatus.CANCELLED
      db.commit()
      return {"message": "Team request cancelled"}
  
  raise HTTPException(status_code=400, detail="No pending team found")

def get_team_status(db: Session, team_id: int, user_id: int):
    last_member_entry = (
        db.query(TeamMember)
        .join(Team)
        .filter(TeamMember.user_id == user_id)
        .order_by(Team.created_at.desc())
        .first()
    )

    if not last_member_entry:
        return {"status": "NONE"}

    team = last_member_entry.team

    if team.status == TeamStatus.PENDING:
        time_diff = datetime.now() - team.created_at
        if time_diff > timedelta(minutes=5):
             team.status = TeamStatus.CANCELLED
             db.commit()
             return {"status": "EXPIRED"}

    return {
        "team_id": team.id,
        "status": team.status.value,
        "members_ready": [m.user_id for m in team.members if m.confirmed]
    }

def dissolve_team_by_user(db: Session, user_id: int):
  team_entry = (
        db.query(Team)
        .join(TeamMember)
        .filter(
            TeamMember.user_id == user_id, 
            Team.status == TeamStatus.ACTIVE
        ).first()
    )

  if not team_entry:
      raise HTTPException(status_code=400, detail="User is not in an active team")

  team_entry.status = TeamStatus.FAILED
  
  db.commit()
  
  return {"message": f"Team {team_entry.id} dissolved due to quiz failure.", "team_id": team_entry.id}
