#!/usr/bin/env bash
set -e

# Ensure scripts are executable and use LF line endings
for f in wait-for-mlflow.sh wait-for-model.sh; do
    [ -f "$f" ] && chmod +x "$f" && sed -i 's/\r$//' "$f"
done

echo "Starting Diabetes API..."

# Wait for MLflow server
./wait-for-mlflow.sh

# Wait for model file
./wait-for-model.sh

# Start FastAPI
exec uvicorn app:app --host 0.0.0.0 --port 8000
