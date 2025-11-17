from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.utils import get_openapi
from dotenv import load_dotenv
import os

from core.database import engine, Base
from routers import test_db
from api.v1 import api_router

from scripts.users import seed_users_from_csv
from scripts.challenge_question import seed_challenge_questions_from_csv


# .env 파일 로드
load_dotenv()

# 간단히 앱 시작 시 테이블 생성 (개발용)
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="Devfactory 친해지길바라",
    description="Devfactory 친해지길바라 API 서버",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    root_path="/api",
)

# Swagger 기본 경로를 /api 로 지정
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(   
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    openapi_schema["servers"] = [{"url": "/api"}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS 미들웨어 설정
origins = os.getenv("CORS_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add TrustedHostMiddleware to handle X-Forwarded-Proto headers

# Add TrustedHostMiddleware to handle X-Forwarded-Proto headers
trusted_hosts = os.getenv("TRUSTED_HOSTS", "*").split(",")
if "*" not in trusted_hosts: # If "*" is present, it means all hosts are allowed, so no need to add "localhost"
    trusted_hosts.append("localhost") # Always allow localhost for development
app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)


app.include_router(api_router, prefix="/v1")
app.include_router(test_db.test_router)


@app.get("/")
async def read_root():
    """루트 엔드포인트"""
    return {
        "message": "Devfactory 친해지길바라 API 서버",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}

# 서버 시작 시 실행
@app.on_event("startup")
def on_startup():
    print("🚀 Server starting, seeding challenge questions...")
    seed_users_from_csv("./scripts/user_data.csv")
    seed_challenge_questions_from_csv("./scripts/challenge_question.csv")
