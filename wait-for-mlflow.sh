#!/bin/sh
MLFLOW_URL=http://mlflow-server:5000
echo "Waiting for MLflow server at $MLFLOW_URL..."
while ! curl -s $MLFLOW_URL >/dev/null; do
    sleep 2
done
echo "MLflow server is up. Starting FastAPI..."
exec "$@"
