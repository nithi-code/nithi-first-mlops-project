#!/usr/bin/env bash
set -e

MODEL_PATH="${MODEL_PATH:-/app/model/diabetes_rf_model.pkl}"

echo "Waiting for model at $MODEL_PATH..."
until [ -f "$MODEL_PATH" ]; do
    echo "Model not found yet. Sleeping 5s..."
    sleep 5
done
echo "Model found!"
