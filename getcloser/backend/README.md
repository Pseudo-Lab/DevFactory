
### Backend 서버 세팅
1. docker 설치
2. docker 빌드: `docker-compose -f docker-compose.yaml up --build`

3. API 서버 접속:
`http://localhost:8000/docs`


### 코드 구조
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