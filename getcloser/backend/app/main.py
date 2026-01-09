from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from dotenv import load_dotenv
import os
import secrets

from core.database import engine, Base
from routers import test_db, admin
from api.v1 import api_router

from scripts.seed import seed_initial_data


# .env 파일 로드
load_dotenv()

# 간단히 앱 시작 시 테이블 생성 (개발용)
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
is_dev = os.getenv("ENV") == "development"
app = FastAPI(
    title="Devfactory 친해지길바라",
    description="Devfactory 친해지길바라 API 서버",
    version="1.0.0",
    docs_url="/docs" if is_dev else None,
    redoc_url="/redoc" if is_dev else None,
    openapi_url="/openapi.json" if is_dev else None,
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
app.include_router(api_router, prefix="/api/v1")
app.include_router(test_db.test_router, prefix="/api/v1")
app.include_router(admin.admin_router, prefix="/api/v1")

security = HTTPBasic(auto_error=False)

def verify_docs_credentials(credentials: HTTPBasicCredentials | None = Depends(security)) -> None:
    if is_dev:
        return

    expected_user = os.getenv("SWAGGER_USER")
    expected_password = os.getenv("SWAGGER_PASSWORD")

    # If credentials aren't configured, keep docs closed by default.
    if not expected_user or not expected_password:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Swagger credentials are not configured.",
        )

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

    is_user_ok = secrets.compare_digest(credentials.username, expected_user)
    is_password_ok = secrets.compare_digest(credentials.password, expected_password)
    if not (is_user_ok and is_password_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )

if not is_dev:
    @app.get("/docs", include_in_schema=False)
    def get_swagger_docs(_: None = Depends(verify_docs_credentials)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="API Docs")

    @app.get("/redoc", include_in_schema=False)
    def get_redoc_docs(_: None = Depends(verify_docs_credentials)):
        return get_redoc_html(openapi_url="/openapi.json", title="API Docs")

    @app.get("/openapi.json", include_in_schema=False)
    def openapi_json(_: None = Depends(verify_docs_credentials)):
        return JSONResponse(
            get_openapi(
                title=app.title,
                version=app.version,
                description=app.description,
                routes=app.routes,
            )
        )


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
    print("🚀 Server starting, seeding initial data...")
    seed_initial_data()
