from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from .routers import certificate


# .env 파일 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="PseudoLab 수료증 발급 시스템",
    description="PseudoLab 수료증 발급을 위한 API 서버",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 미들웨어 설정
origins = os.getenv("CORS_ORIGINS", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(certificate.certificate_router)

@app.get("/")
async def read_root():
    """루트 엔드포인트"""
    return {
        "message": "PseudoLab 수료증 발급 시스템 API 서버",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
