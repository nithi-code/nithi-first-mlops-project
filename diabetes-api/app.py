from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import mlflow
import os
from datetime import datetime

MODEL_PATH = os.getenv("MODEL_PATH", "/app/model/diabetes_rf_model.pkl")
EXPERIMENT_NAME = "Diabetes-Prediction-Inference"

app = FastAPI(title="Diabetes Prediction API", version="1.0")

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train it first!")

model = joblib.load(MODEL_PATH)

class DiabetesInput(BaseModel):
    Pregnancies: int
    Glucose: float
    BloodPressure: float
    BMI: float
    Age: int

@app.get("/")
def home():
    return {"message": "Diabetes Prediction API is running."}

@app.post("/predict")
def predict(data: DiabetesInput):
    features = np.array([[data.Pregnancies, data.Glucose, data.BloodPressure, data.BMI, data.Age]])
    prediction = int(model.predict(features)[0])
    probability = float(model.predict_proba(features)[0][1])

    # Log inference
    mlflow.set_experiment(EXPERIMENT_NAME)
    with mlflow.start_run(run_name="inference", nested=True):
        for k, v in data.dict().items():
            mlflow.log_param(k, v)
        mlflow.log_metric("predicted_label", prediction)
        mlflow.log_metric("predicted_probability", probability)
        mlflow.set_tag("inference_time", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    return {
        "prediction": prediction,
        "probability_diabetes": round(probability, 4),
        "input_data": data.dict()
    }
