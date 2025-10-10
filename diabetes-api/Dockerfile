# Python slim image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --disable-pip-version-check -r requirements.txt

# Copy app code
COPY app.py /app/

# Copy scripts and make executable
COPY wait-for-mlflow.sh wait-for-model.sh start-api.sh /app/
RUN chmod +x /app/wait-for-mlflow.sh \
    && chmod +x /app/wait-for-model.sh \
    && chmod +x /app/start-api.sh

# Expose FastAPI port
EXPOSE 8000

# Start the API
CMD ["./start-api.sh"]
