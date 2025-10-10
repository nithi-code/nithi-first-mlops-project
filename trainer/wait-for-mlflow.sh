#!/usr/bin/env bash
set -e

MLFLOW_URI="${MLFLOW_TRACKING_URI:-http://mlflow-server:5000}"

echo "Waiting for MLflow server at $MLFLOW_URI..."
until curl -s "$MLFLOW_URI"/api/2.0/mlflow/experiments/list >/dev/null 2>&1; do
    echo "MLflow not ready yet. Sleeping 5s..."
    sleep 5
done
echo "MLflow server is ready!"
