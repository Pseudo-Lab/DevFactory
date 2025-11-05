
### Backend 서버 세팅
1. docker 설치
2. 프로젝트 루트(`getcloser/`)에서 도커 빌드 및 실행: `docker compose up --build`

3. API 문서:
`http://localhost:${BACKEND_PORT:-8000}/docs`

4. 초기 구성:
- FastAPI 기반 REST API 서버
- PostgreSQL (Docker) 연결 및 SQLAlchemy 지원
- `/test/ping_db` 엔드포인트로 DB 연결 상태 확인
- `/health` 헬스체크, `/` 루트 상태 응답


### 실행 전 준비 (.env)
`getcloser/` 루트에 환경변수를 정의한 `.env` 파일을 생성하세요. 없으면 일부 기본값이 적용됩니다.

예시:
```
# 서버
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:5173

# Postgres (docker-compose의 db 서비스와 일치)
DB_USER=app_user
DB_PASSWORD=app_password
DB_DATABASE=app_db

# 애플리케이션 설정
SECRET_KEY=secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60

# 선택: 직접 연결문자열을 쓰고 싶다면 아래로 덮어쓰기
# DATABASE_URL=postgresql+psycopg2://app_user:app_password@db:5432/app_db
```

### 실행 방법
프로젝트 루트(`getcloser/`)에서 아래 명령을 실행하세요.

```
docker compose up --build
```

정상 실행 시:
- 백엔드: `http://localhost:${BACKEND_PORT:-8000}`
- 문서: `http://localhost:${BACKEND_PORT:-8000}/docs`
- DB는 내부 네트워크에서 호스트명 `db`, 포트 `5432`로 접근합니다.


### 유용한 엔드포인트
- `/` : 서버 상태
- `/health` : 헬스 체크
- `/test/ping_db` : DB 연결 확인 (SELECT 1)


### Backend 폴더 구조
```
.
├── Dockerfile
├── README.md
└── src
    ├── __init__.py
    ├── assets
    ├── config.py
    ├── database.py
    ├── main.py
    ├── models
    ├── requirements.txt
    ├── routers
    │   └── test_db.py
    ├── services
    └── utils
```