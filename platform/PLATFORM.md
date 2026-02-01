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
`platform` 디렉토리 루트에 `.env` 파일을 생성하고 정보를 입력합니다.
> [!WARNING]
> `.env` 파일은 데이터베이스 접속 정보 등 민감한 정보를 포함하므로 절대 Git 저장소에 커밋하지 마세요. (이미 `.gitignore`에 포함되어 있습니다.)

```bash
# .env 파일 예시
APP_HOST=your-domain.com

# Database
# 형식: postgresql://[user]:[password]@[host]:[port]/[dbname]
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
```

### 4. Local Development
로컬 환경에서 개발 시 코드 변경사항을 즉시 확인(Hot-Reloading)하려면 `docker-compose.dev.yml` 오버라이드 파일을 사용합니다.

```bash
cd platform
# 개발 모드로 실행 (소스 코드 수정 시 즉시 반영)
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

### 5. Traefik 기반 배포 (Production)
운영 서버 환경에서 Docker Compose를 사용하여 서비스를 빌드하고 실행합니다.
```bash
cd platform
# 전체 서비스 빌드 및 실행
docker compose up -d --build
```

#### 배포 확인
- **Frontend (Web)**: `https://<APP_HOST>`
- **Backend (API)**: `https://<APP_HOST>/api/health`

### 6. Security & Logging
- **Logging**: 본 플랫폼은 방문자 추적을 위해 `logging.access_log` 테이블을 사용합니다. 상세 스키마는 내부 데이터베이스 관리 문서를 참조하세요.
- **API Security**: `/api/stats` 관련 엔드포인트는 데이터 적재 및 조회를 위해 공개되어 있습니다. 필요 시 특정 도메인(CORS) 제한이나 Rate Limiting을 적용하는 것을 권장합니다.
- **Credential Management**: 운영 환경에서는 정기적으로 데이터베이스 비밀번호를 변경하고 `.env` 관리에 유의하세요.

### 7. Verification
- Traefik 대시보드에서 `df-platform` 관련 라우터가 활성화되었는지 확인하세요.
- 브라우저에서 사이트 접속 시 HTTPS 상시 연결 및 방문 기록 적재 여부를 확인하세요.
