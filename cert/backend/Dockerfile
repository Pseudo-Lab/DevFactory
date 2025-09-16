# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install tzdata and set timezone to Asia/Seoul
RUN apt-get update && \
    apt-get install -y --no-install-recommends tzdata && \
    ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV TZ=Asia/Seoul

# Copy the dependency files
COPY requirements.txt .
COPY uv.lock .

# Install any needed packages specified in requirements.txt
# Using uv pip install for faster and more reliable dependency management
RUN pip install uv && uv pip install --system -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "src.main:app"]
