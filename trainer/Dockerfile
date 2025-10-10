# Base image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy training script
COPY train_diabetes_model.py /app/

# Copy model folder to save trained model
RUN mkdir -p /app/model

CMD ["python", "train_diabetes_model.py"]
