# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install curl and other dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Make wait scripts executable
RUN chmod +x wait-for-model.sh wait-for-mlflow.sh

# Expose FastAPI port
EXPOSE 8000

# Default command (overridden by docker-compose)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
