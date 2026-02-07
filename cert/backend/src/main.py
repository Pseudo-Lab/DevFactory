import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import certificate
from .routers.logging import logging_router
from .utils.access_log import access_log_middleware, close_access_log, init_access_log


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

environment = os.getenv("ENVIRONMENT", "dev").lower()
hide_docs = environment.startswith("prod")

# FastAPI 앱 생성
app = FastAPI(
    title="PseudoLab 수료증 발급 시스템",
    description="PseudoLab 수료증 발급을 위한 API 서버",
    version="1.0.0",
    docs_url=None if hide_docs else "/docs",
    redoc_url=None if hide_docs else "/redoc",
    openapi_url=None if hide_docs else "/openapi.json",
)

# Access log middleware
app.middleware("http")(access_log_middleware)

# CORS configuration
# Load allowed origins from CORS_ORIGINS environment variable (comma-separated)
cors_origins_str = os.getenv("CORS_ORIGINS", "")
if cors_origins_str:
    origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]
else:
    # Default origins for local development and known production/dev domains
    origins = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://cert.pseudo-lab.com",
        "https://dev-cert.pseudolab-devfactory.com",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 모든 환경에서 /api 프리픽스 사용 (개발/프로덕션 통일)
app.include_router(certificate.certificate_router, prefix="/api")
app.include_router(logging_router, prefix="/api")
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


@app.on_event("startup")
async def setup_access_log():
    await init_access_log(app)


@app.on_event("shutdown")
async def teardown_access_log():
    await close_access_log(app)
