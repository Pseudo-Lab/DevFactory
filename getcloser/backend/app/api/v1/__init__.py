from api.v1.auth import auth
from api.v1.users import users
from api.v1.challenges import challenges
from api.v1.teams import teams
from core.dependencies import get_current_user
from fastapi import APIRouter, Depends

private_router = APIRouter(
  dependencies=[Depends(get_current_user)]
)
private_router.include_router(users.router, prefix="/users", tags=["users"])
private_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
private_router.include_router(teams.router, prefix="/teams", tags=["teams"])

public_router = APIRouter()
public_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router = APIRouter()
api_router.include_router(public_router)
api_router.include_router(private_router)
