# 🛠️ DevFactory Contributing Guide

> Last updated: 2025-11-05
> 
> 
> Maintainer: **DevFactory Team**
> 

---

## 🧭 Branch Strategy

DevFactory는 **모노레포(Monorepo)** 구조를 사용합니다.

여러 서비스(`getcloser`, `cert-system`)를 하나의 리포지토리에서 관리하며,

일부 프로젝트(`JobPT`, `event-bingo`)는 **별도 리포지토리**로 운영합니다.

| 브랜치 | 역할 | 비고 |
| --- | --- | --- |
| `main` | 프로덕션 통합 | 전체 서비스의 통합 및 배포용 브랜치 |
| `feat/*` | 기능 개발 | 서비스별 기능 단위 개발 브랜치 |
| `fix/*` | 버그 수정 | 서비스별 버그 수정 브랜치 |
| `docs/*` | 문서 수정 | README, CONTRIBUTING 등 문서 전용 브랜치 |

> 브랜치명 예시
> 
> - `feat/getcloser/auto-deploy`
> - `fix/getcloser/auth-refresh`
> - `docs/getcloser/update-deploy-guide`
> - `chore/devfactory/github-actions-update`

---

## ⚙️ Workflow

1. **기능 개발 브랜치 생성**
    
    ```bash
    git checkout main
    git checkout -b feat/<feature-name>
    # 예시
    git checkout -b feat/auto-deploy
    ```
    
2. **기능 구현 및 커밋**
    
    ```bash
    git commit -m "feat(getcloser): add CI/CD auto deploy pipeline"
    ```
    
3. **PR 생성**
    
    ```bash
    git push origin feat/auto-deploy
    ```
    
    - `feat/*` → `main`으로 PR 생성
    - PR 제목은 작업 목적을 명확히 작성
    예: `fix(getcloser): resolve API timeout issue`
4. **리뷰 및 병합**
    - 코드 리뷰 및 승인 후 병합
    - 이후 브랜치는 **삭제 권장** (`Delete branch after merge`)
    - 자세한 내용은 병합 및 리뷰 규칙 참고

---

## 🪶 Commit Convention

모든 커밋은 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 규칙을 따릅니다.

```bash
<type>(<scope>): <short summary>
```

| Type | 설명 |
| --- | --- |
| `feat` | 새로운 기능 추가 |
| `fix` | 버그 수정 |
| `docs` | 문서 변경 (README, CONTRIBUTING 등) |
| `chore` | 빌드, 의존성, 설정 등 변경 (비즈니스 로직 영향 없음) |
| `refactor` | 코드 리팩토링 |
| `test` | 테스트 코드 추가 또는 수정 |
| `perf` | 성능 개선 |

> 커밋 예시
> 
> - `feat(getcloser): add automatic deploy pipeline`
> - `fix(getcloser): handle login token issue`
> - `docs(devfactory): update contributing guide`

---

## 🔀 Merge & Review Rules

- **직접 push 금지** (`main` 브랜치 포함)
- 모든 변경은 **Pull Request(PR)**를 통해 진행
- **리뷰어 1인 이상 승인 필수**
- **PR 작성자가 직접 병합 (rebase merge 권장)**
- **병합 후 브랜치 삭제 권장**
- **CI 통과 필수** (`lint`, `test`, `build`)

> 💡 PR 생성 시 needs-review, 병합 시 merged 라벨이 자동으로 부여됩니다.
> 

---

## ✅ Pull Request Guide

1. **PR 제목 규칙**
    
    ```
    feat(getcloser): add deploy pipeline
    fix(getcloser): resolve API error
    docs(devfactory): update contributing guide
    
    ```
    
2. **PR 본문 템플릿**
    - **요약:** 변경 내용을 간략히 설명
    - **관련 이슈:** `Closes #123`
    - **테스트 결과:** 검증 방법 명시
    - **스크린샷 (선택):** UI 변경 시 첨부

---

## 🔒 Security & Environment Files

- `.env`, API 키, 비밀번호 등 **민감한 정보 커밋 금지**
- `.env.example`만 Git에 포함
- 실제 환경 변수는 GitHub **Secrets / Variables**에서 관리

---

## 💡 Workflow Example

```bash
# 1. 기능 브랜치 생성
git checkout main
git checkout -b feat/auto-deploy

# 2. 작업 및 커밋
git commit -m "feat(getcloser): add CI/CD pipeline"

# 3. 원격 푸시 & PR 생성
git push origin feat/auto-deploy

# 4. PR 생성 → 'needs-review' 자동 부여
# 5. 리뷰 승인 → rebase merge → 'merged' 자동 부여
# 6. 브랜치 삭제

```

---

## 📘 Notes

- 주요 서비스: `getcloser`, `cert-system`
- 별도 리포지토리: `JobPT`, `event-bingo`
