# ------------------------------- 
# Build Stage // Next.js 빌드 전용 스테이지
# -------------------------------
FROM node:24-alpine AS builder

# 프로덕션 모드 설정 및 Next.js 텔레메트리(익명 통계) 비활성화
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

# 작업 디렉토리 /app 지정
WORKDIR /app

# 시스템 의존성 설치
RUN apk add --no-cache libc6-compat

# package.json과 lock 파일 복사
COPY package*.json ./

# 개발 의존성(devDependencies) 포함 설치
RUN npm i --include=dev

# 소스 코드 복사
COPY . .

# Next.js 프로젝트 빌드
RUN npm run build


# ------------------------------- 
# Runner  Stage // 실제 서비스 실행 스테이지
# -------------------------------
FROM node:24-alpine AS runner

# 런타임 환경 변수 설정
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

# 작업 디렉토리 /app 지정
WORKDIR /app

# 시스템 의존성 설치
RUN apk add --no-cache libc6-compat

# package.json과 lock 파일 복사
COPY package*.json ./

# 프로덕션 의존성만 설치 + 캐시 정리
RUN npm i --omit=dev && npm cache clean --force

# 빌드 스테이지에서 생성된 산출물만 복사
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# 사용자 생성 및 권한 설정
RUN addgroup --system --gid 1001 nodejs \
 && adduser --system --uid 1001 nextjs \
 && mkdir -p .next/cache/images \
 && chown -R nextjs:nodejs /app

 # 보안 강화를 위해 nextjs 유저로 실행
USER nextjs

# Next.js 프로덕션 서버 실행
CMD ["npm", "run", "start"]
