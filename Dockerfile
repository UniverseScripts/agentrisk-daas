FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system dependencies if required
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app

# Expose port (Render defaults to PORT environment variable or 10000)
ENV PORT=10000
EXPOSE 10000

# Start FastAPI server
CMD uvicorn api.main:app --host 0.0.0.0 --port $PORT --workers 2