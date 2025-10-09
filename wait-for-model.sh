#!/bin/sh
MODEL_PATH=/app/model/diabetes_rf_model.pkl
echo "Waiting for model at $MODEL_PATH..."
while [ ! -f $MODEL_PATH ]; do sleep 1; done
echo "Model found. Starting FastAPI..."
exec "$@"
