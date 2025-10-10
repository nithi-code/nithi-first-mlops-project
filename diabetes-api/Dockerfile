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
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py /app/

# Copy shell scripts
COPY start-api.sh wait-for-mlflow.sh wait-for-model.sh /app/

# Ensure scripts have LF line endings (important for Windows hosts)
RUN sed -i 's/\r$//' /app/*.sh && \
    chmod +x /app/start-api.sh \
    && chmod +x /app/wait-for-mlflow.sh \
    && chmod +x /app/wait-for-model.sh

# Expose FastAPI port
EXPOSE 8000

# Start the API
CMD ["/app/start-api.sh"]
