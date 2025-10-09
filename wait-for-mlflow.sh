#!/bin/sh
MLFLOW_URL=${MLFLOW_TRACKING_URI:-http://mlflow-server:5000}

echo "Waiting for MLflow server at ${MLFLOW_URL}..."
while ! curl -s "${MLFLOW_URL}/api/2.0/mlflow/experiments/list" > /dev/null 2>&1; do
    echo "MLflow not ready yet. Sleeping 5s..."
    sleep 5
done
echo "MLflow server is ready!"
