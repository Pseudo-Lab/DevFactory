### 0. LLM Model Download

### 1. Docker 개념 및 필요성 (15분)

- 컨테이너와 이미지의 개념
- Docker가 왜 필요한가 (부제 : 저는 잘 되는데요?) (환경 재현, 배포 편의성 등)

### 2. Docker 기본 명령어 실습 (15분)

- 간단한 커스텀 컨테이너 제공 (pytorch example)
- `docke build & run` , `ps`, `exec`, `logs` 등
- 컨테이너 상태 확인 및 진입 실습

### 3. Docker compose (30분)

- Docker Compose 개념 소개
    - 복수 컨테이너를 하나의 구성 파일로 정의
    - `docker run`을 반복하지 않아도 됨
- `docker-compose.yaml` 구조 설명
    - `services`, `volumes`, `ports`, `depends_on` 등 필수 필드
- 간단한 예제 실습
    - 예: nginx + html 서버, 또는 redis + flask 등
- 명령어 실습
    - `docker compose up`, `down`, `ps`, `logs`, `restart` 등
- 정리: 단일 명령으로 여러 컨테이너 구성 및 실행

### 4. Ollama 실행 (Docker 사용) (20분)

- `docker run`으로 Ollama 실행
- 로컬 LLM API 호출

### 5. Web UI 실행 (15분)

- Open WebUI 컨테이너 실행
- 브라우저에서 로컬 ChatGPT 환경 접속

### 6. Docker Compose로 통합 구성 (30분)

- `docker-compose.yaml` 작성
- Ollama + WebUI를 함께 실행
- 구성 이해 및 명령어 정리

### 7. Q&A