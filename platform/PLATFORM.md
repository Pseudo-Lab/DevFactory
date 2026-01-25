# DevFactory Unified Platform

소개 페이지와 백엔드 API가 통합된 DevFactory의 메인 플랫폼 관리 가이드입니다. 
본 설정은 **Traefik 역방향 프록시**를 사용하는 서버 환경을 전제로 합니다.

### 1. Production Build
로컬 또는 서버에서 프론트엔드 에셋을 빌드합니다.
```bash
cd platform/frontend
npm install
npm run build
```
결과물은 `platform/frontend/dist` 디렉토리에 생성됩니다.

### 2. Deployment Options

#### Option A: Static Hosting (GitHub Pages / Vercel)
단순 웹 페이지(Frontend)만 배포하고 싶은 경우에 사용합니다.
1. `platform/frontend`에서 `npm run build`를 실행합니다.
2. `dist` 폴더 내의 파일들을 배포 서비스에 업로드합니다.
> **참고**: 이 방식으로는 자체 DB 방문자 추적 기능을 사용할 수 없습니다.

#### Option B: Unified Platform (Full-Stack / Docker)
방문자 추적 기능을 포함한 전체 플랫폼 배포 방식입니다. **(권장)**

### 3. Environment Setup
`platform` 디렉토리 루트에 `.env` 파일을 생성하고 서버 환경에 맞게 정보를 입력합니다.
```bash
# .env 파일 예시
APP_HOST=intro.pseudolab-devfactory.com

# Database
DATABASE_URL=postgresql://user:pass@devfactory-postgres:5432/dbname
```

### 3. Traefik 기반 배포
Docker Compose를 사용하여 서비스를 실행합니다.
```bash
cd platform
# 전체 서비스 빌드 및 실행
docker-compose up -d --build
```

#### 배포 확인
- **Frontend (Web)**: `https://<APP_HOST>`
- **Backend (API)**: `https://<APP_HOST>/api/health`

### 4. Database Schema
사용 중인 `logging.access_log` 테이블의 구조는 다음과 같아야 합니다.
```sql
CREATE TABLE logging.access_log (
    id SERIAL PRIMARY KEY,
    ts TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    path TEXT NOT NULL,
    method TEXT NOT NULL,
    status INTEGER NOT NULL,
    latency_ms INTEGER,
    ip_hash TEXT,
    user_agent TEXT,
    referrer TEXT
);
```

### 5. Verification
- Traefik 대시보드에서 `df-platform` 관련 라우터가 활성화되었는지 확인하세요.
- 브라우저에서 사이트 접속 시 HTTPS 상시 연결 및 방문 기록 적재 여부를 확인하세요.
