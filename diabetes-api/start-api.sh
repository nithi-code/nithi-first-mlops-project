#!/bin/sh
# Wrapper script to start FastAPI only after MLflow & model are ready

# Wait for MLflow
./wait-for-mlflow.sh

# Wait for trained model
./wait-for-model.sh

# Start FastAPI
uvicorn app:app --host 0.0.0.0 --port 8000
