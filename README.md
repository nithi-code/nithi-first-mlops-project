# Diabetes Prediction API with FastAPI & MLflow

A full **MLOps pipeline** for predicting diabetes risk using a Random Forest model, with:

- Model training & metrics logging using **MLflow**
- Prediction API using **FastAPI**
- Containerized deployment with **Docker & Docker Compose**
- Windows-compatible wait scripts

---

## Features

- **Train a model** and log metrics/parameters to MLflow
- **Serve predictions** via FastAPI (`/predict`)  
- Logs all **API requests & predictions to MLflow** for tracking
- Fully containerized for **reproducible deployment**
- Wait scripts ensure **MLflow and model are ready** before API starts


## Project Structure
```
nithi-first-mlops-project/
├── app.py # FastAPI API
├── train_diabetes_model.py # Model training + MLflow logging
├── Dockerfile # Container image definition
├── docker-compose.yml # Compose for MLflow, trainer, API
├── requirements.txt # Python dependencies
├── wait-for-model.sh # Wait for model before API start
├── wait-for-mlflow.sh # Wait for MLflow server before API start
├── model/ # Saved model artifacts
├── mlruns/ # MLflow experiment/artifacts storage
└── mlflow/ # SQLite DB storage for MLflow
```

## Prerequisites

- **Docker Desktop** installed and running
- **Windows** users: ensure project folder is shared with Docker
- Internet access to download dataset (`diabetes.csv` from GitHub)

---

## Setup

### 1️⃣ Create required folders

```bash
mkdir mlflow mlruns model
```

2️⃣ Build and start Docker containers
```bash
docker compose up --build
```
mlflow-server → MLflow tracking server

trainer → Trains Random Forest model and logs metrics

diabetes-api → FastAPI server waits for MLflow + model

## API Usage

### Base URL

```bash
http://localhost:8000
```

#### Example /predict Request
```json
POST /predict
{
  "Pregnancies": 2,
  "Glucose": 90,
  "BloodPressure": 80,
  "BMI": 25,
  "Age": 45
}
```

### Example Response

```json
{
  "prediction": 0,
  "probability_diabetes": 0.1403,
  "input_data": {
    "Pregnancies": 2,
    "Glucose": 90,
    "BloodPressure": 80,
    "BMI": 25,
    "Age": 45
  }
}
```

1. prediction: 0 → No diabetes, 1 → Diabetes

2. probability_diabetes: Model confidence for class 1 (diabetes)

3. input_data: Echoed input features

## MLflow UI

### Access MLflow UI:

```bash
http://localhost:5000
```
#### Tracks:

  * Training experiment: parameters, metrics, model artifacts

  * Inference logs: input features, predicted label, probability, timestamp

