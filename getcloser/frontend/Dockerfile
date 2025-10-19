# 1) Builder stage
FROM node:20-alpine AS builder

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache libc6-compat

# Install dependencies
COPY package*.json ./
RUN npm ci --include=dev

# Copy source and build
COPY . .
RUN npm run build

# 2) Runner stage
FROM node:20-alpine AS runner

ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PORT=3000 \
    HOSTNAME=0.0.0.0

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache libc6-compat

# Install production dependencies only
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Copy build artifacts from builder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
USER nextjs

EXPOSE 3000

CMD ["npm", "run", "start"]