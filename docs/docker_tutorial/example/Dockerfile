# 1. 베이스 이미지 설정
#    - Python 3.9 런타임을 제공하는 공식 이미지
#    - 불필요한 파일을 제거해 용량을 줄인 슬림(slim) 버전 사용
FROM python:3.9-slim

# 2. 작업 디렉터리 생성 및 설정
#    - 컨테이너 내에서 이후 명령이 실행될 기본 디렉터리
WORKDIR /app

# 3. 애플리케이션 코드와 의존성 파일 복사
#    - 로컬의 example.py 파일을 컨테이너의 /app 디렉터리로 복사
COPY example.py .

# 4. 필수 라이브러리 설치
#    - example.py 실행에 필요한 numpy 패키지를 설치
#    - 캐시를 남기지 않는 옵션(--no-cache-dir)으로 이미지 크기 최적화
RUN pip install --no-cache-dir numpy

# 5. 컨테이너 시작 시 실행할 명령어 지정
#    - 컨테이너가 기동되면 자동으로 example.py 스크립트 실행
CMD ["python", "example.py"]