# Use an official Python runtime as a parent image
FROM python:3.11-slim

# 기본 Python 런타임 환경 변수
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    TZ=Asia/Seoul \
    VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:${PATH}"

# Set the working directory in the container
WORKDIR /app

# Install tzdata and set timezone to Asia/Seoul
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata libgl1 libglib2.0-0 && \
    ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# install uv for improved package management
RUN pip install --no-cache-dir "uv>=0.5.0"

# Copy only the dependency files to leverage Docker cache
COPY pyproject.toml uv.lock ./

# Install the dependencies into the project virtualenv
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "src.main:app"]
