# Stage 1: Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy project files and build
COPY . .
RUN npm run build

# Stage 2: Serve stage
FROM nginx:stable-alpine as production-stage

# Copy built assets from build-stage to nginx
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
