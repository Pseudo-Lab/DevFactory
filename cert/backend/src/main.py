import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import certificate


def configure_logging() -> None:
    """기본 로깅 설정을 구성한다."""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )


# .env 파일 로드 및 로깅 설정
load_dotenv()
configure_logging()
logger = logging.getLogger(__name__)

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모든 환경에서 /api 프리픽스 사용 (개발/프로덕션 통일)
app.include_router(certificate.certificate_router, prefix="/api")
logger.info("FastAPI app initialized", extra={"environment": os.getenv("ENVIRONMENT")})


@app.get("/")
async def read_root():
    """루트 엔드포인트"""
    return {
        "message": "PseudoLab 수료증 발급 시스템 API 서버",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
