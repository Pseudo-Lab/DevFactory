# GitHub 풀 리퀘스트 가이드

## 1. 소개
**Pull Request(PR)**는 저장소에서 변경 사항을 제안하고 다른 사람들과 협업하는 방법입니다. PR을 통해 코드를 병합하기 전에 코드 검토를 받을 수 있습니다.

## 2. 환경 설정
### Git 설치
```sh
# Git 설치 (Linux)
sudo apt install git

# Git 설치 (MacOS)
brew install git

# Git 설치 (Windows)
# https://git-scm.com/ 에서 다운로드 후 설치
```

### Git 설정
```sh
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### 저장소 클론(Clone)
![](../assets/imgs/github-clone.png)
```sh
git clone "저장소 주소"
```

### 저장소 포크(Fork)
1. GitHub에서 저장소로 이동합니다.
![](../assets/imgs/github-main.png)

2. 오른쪽 상단의 **Fork** 버튼을 클릭합니다.

## 3. 브랜치 생성
```sh
# 포크한 저장소 클론
git clone https://github.com/your-username/repository.git
cd repository

# 새 브랜치 생성 및 전환
git checkout -b feature-branch
```

## 4. 변경 사항 적용
```sh
# 파일 수정하기
nano file.txt  # 파일을 편집

# 변경 사항 스테이징 및 커밋
git add file.txt
git commit -m "새 기능 추가"
```

## 5. 변경 사항을 GitHub에 푸시
```sh
git push origin feature-branch
```

## 6. Pull Request 생성
1. GitHub에서 저장소로 이동합니다.
2. **Pull Requests** → **New Pull Request** 클릭.
3. 브랜치를 선택하고 변경 사항을 확인합니다.
4. **Create Pull Request** 버튼을 클릭하고 제목과 설명을 추가합니다.
5. 검토자를 추가하고 제출합니다.

## 7. PR 리뷰 및 업데이트
```sh
# 최신 변경 사항 가져오기
git fetch origin

# 브랜치 체크아웃 후 수정
git checkout feature-branch
nano file.txt  # 파일 수정

# 커밋 수정 또는 새 커밋 생성
git add file.txt
git commit --amend -m "기능 세부사항 업데이트"

# 변경 사항 푸시
git push origin feature-branch --force
```

## 8. Pull Request 병합
PR이 승인되면 다음 단계로 병합할 수 있습니다:
1. GitHub에서 **Merge Pull Request** 버튼 클릭.
2. 더 이상 필요하지 않은 경우 브랜치를 삭제합니다.

## 9. 병합 충돌 해결
```sh
# 최신 변경 사항 가져오기
git checkout main
git pull origin main

# 기능 브랜치 병합
git merge feature-branch

# 충돌 해결 후 파일 스테이징
git add conflicted-file.txt
git commit -m "병합 충돌 해결"
```

## 10. 고급 기능
### GitHub CLI 사용
```sh
# CLI를 사용하여 PR 생성
gh pr create --base main --head feature-branch --title "새 기능" --body "변경 사항 설명"
```

## 11. 결론
- 의미 있는 커밋 메시지를 사용하고, 작은 PR을 유지하며, 조기에 리뷰를 요청하세요.
- 브랜치를 최신 상태로 유지하고 충돌을 효과적으로 해결하세요.
- GitHub Actions를 활용하여 Git 워크플로우를 자동화하는 방법도 고려해 보세요.
