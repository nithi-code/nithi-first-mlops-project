from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import mlflow
import os
from datetime import datetime
import logging
import time
from mlflow.exceptions import MlflowException

# ==== Logging setup ====
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ==== Model path & experiment ====
MODEL_PATH = "model/diabetes_rf_model.pkl"
EXPERIMENT_NAME = "Diabetes-Prediction-Inference"

# ==== Load trained model ====
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train it first using train_diabetes_model.py")
model = joblib.load(MODEL_PATH)

# ==== Initialize FastAPI ====
app = FastAPI(
    title="Diabetes Prediction API with MLflow Logging",
    description="Predicts diabetes outcome and logs requests/responses to MLflow",
    version="1.1.0"
)

# ==== Define input schema ====
class DiabetesInput(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    BMI: float
    Age: int

# ==== MLflow logging with retry ====
def log_to_mlflow(params, metrics):
    mlflow.set_experiment(EXPERIMENT_NAME)
    for _ in range(5):  # retry up to 5 times
        try:
            with mlflow.start_run(run_name="inference_log", nested=True):
                for k, v in params.items():
                    mlflow.log_param(k, v)
                for k, v in metrics.items():
                    mlflow.log_metric(k, v)
                mlflow.set_tag("inference_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                mlflow.set_tag("source", "FastAPI")
            break
        except MlflowException:
            time.sleep(2)

@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running with MLflow logging."}

@app.post("/predict")
def predict(data: DiabetesInput):
    # Preserve feature names
    features = pd.DataFrame([data.dict()])
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])

    # Log to container logs
    logger.info(f"Received request: {data.dict()}")
    logger.info(f"Prediction: {prediction}, Probability: {probability}")

    # Log to MLflow with retry
    log_to_mlflow(data.dict(), {"predicted_label": prediction, "predicted_probability": probability})

    return {
        "prediction": prediction,
        "probability_diabetes": round(probability, 4),
        "input_data": data.dict()
    }
