
# 🛠️ DevFactory Contributing Guide

## 1. 브랜치 전략
- 기본 브랜치: `main`, `dev`
- 작업 브랜치: `feat/`, `fix/`, `docs/` 등 prefix 사용
  - 예시: `feat/login`, `fix/navbar-crash`
- 머지는 `PR(Pull Request)`를 통해 진행

## 2. 커밋 메시지 규칙
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 형식 사용
   ```
   <type> <short summary>
   │           │
   │           └─⫸ Summary in present tense. Not capitalized. No period at the end.
   │
   └─⫸ Commit Type: build|ci|docs|feat|fix|perf|refactor|test
   ```
- Commit type (ex: feat: commit message)
   ```
   build: Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
   ci: Changes to our CI configuration files and scripts (examples: CircleCi, SauceLabs)
   docs: Documentation only changes
   feat: A new feature
   fix: A bug fix
   perf: A code change that improves performance
   refactor: A code change that neither fixes a bug nor adds a feature
   test: Adding missing tests or correcting existing tests
   ```

## 3. PR(Pull Request) 규칙
- PR 제목은 작업 목적이 드러나도록 작성
- PR 설명에 **작업 내용**, **관련 이슈**, **스크린샷** 등 포함
- 최소 1명 이상의 리뷰어 승인 후 머지
   - 상황에 따라 유동적으로 적용
- 리뷰 후 **본인이 머지 진행**

## 4. 코드 품질
- Lint, Test는 PR 전에 반드시 통과
- CI 자동 검사(GitHub Actions 등) 적용

## 5. Issue 관리(선택)
- 작업 시작 전 관련 이슈 생성 또는 연결
- 라벨(label) 지정: `bug`, `feature`, `question`, `urgent` 등
- 완료된 이슈는 PR과 함께 자동 닫힘 (`Fixes #이슈번호`)

## 6. 보안 및 환경 변수
- `.env` 파일 또는 민감한 정보는 Git에 커밋 금지
- `gitignore`에 포함된 파일 목록 확인 필수
- 필요시 `.env.example` 제공



## EX) 예시 워크플로우
1. `dev` 브랜치 최신 상태로부터 작업 브랜치 생성  
   `git checkout -b feat/search dev`

2. 기능 개발 및 커밋  
   `git commit -m "feat: 검색 기능 구현"`

3. 원격 푸시 및 PR 생성  
   `git push origin feat/search`

4. `feat/search` -> `dev` PR 생성 → 리뷰어 지정 → 리뷰 후 머지  
   `main` 브랜치는 배포용으로만 사용
