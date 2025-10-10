# Use a slim Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements.txt . 

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy training script only (no extra scripts needed)
COPY train_diabetes_model.py /app/

# Copy model & mlruns volumes if needed (optional)
VOLUME ["/app/model", "/app/mlruns"]

# Set environment variable for MLflow
ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000

# Run the training script
CMD ["python", "train_diabetes_model.py"]
