from api.v1.users import users
from api.v1.challenge import assign_challenge
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(assign_challenge.router, prefix="/challenge", tags=["challenge"])
