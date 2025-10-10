#!/bin/sh
MLFLOW_URI=${MLFLOW_TRACKING_URI:-http://mlflow-server:5000}

echo "Waiting for MLflow server at $MLFLOW_URI..."
until curl -s $MLFLOW_URI > /dev/null; do
  echo "MLflow not ready yet. Sleeping 5s..."
  sleep 5
done
echo "MLflow server is ready!"
