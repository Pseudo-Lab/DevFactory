
### Backend 서버 세팅
1. docker 설치
2. docker 빌드: `docker-compose -f docker-compose.yaml up --build`

3. API 서버 접속:
`http://localhost:8000/docs`

4. 초기 구조:
- FastAPI 기반 REST API 서버
- PostgreSQL 연결 및 ORM 지원
- `/test/ping_db` 엔드포인트를 통한 DB 연결 상태 확인


### 폴더 구조
```
.
├── docker-compose.yaml
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