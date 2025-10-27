from api.v1.users import users
from api.v1.teams import teams
from api.v1.challenges import challenges
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(challenges.router, prefix="/challenges", tags=["challenges"])
