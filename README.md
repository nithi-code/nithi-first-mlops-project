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

---

## Services

| Service    | URL                     |
| ---------- | ----------------------- |
| Diabetes Prediction API  | `http://localhost:8000/docs` |
| MLflow     | `http://localhost:5000` |
| Prometheus | `http://localhost:9090` |
| Grafana    | `http://localhost:3000` |
| Jenkins    | `http://localhost:8081/jenkins` |

* **Model Service:** Flask app serving `/predict` endpoint with Swagger UI and Prometheus metrics.
* **MLflow:** Model tracking server.
* **Prometheus:** Metrics collection.
* **Grafana:** Visualization dashboards.
* **Jenkins:** CI/CD server.

---

## Project Structure
```
nithi-first-mlops-project/
│
├── README.md
├── LICENSE
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── Jenkinsfile
│
├── scripts/                       # helper scripts
│   ├── wait-for-mlflow.sh
│   ├── wait-for-model.sh
│   └── validate_data.py
│
├── requirements.txt
│
├── mlflow/                         # MLflow server storage / configuration
│   └── (e.g. backend_db, artifacts store configuration)
│
├── mlruns/                         # MLflow run logs & artifacts
│
├── data/                           # raw / processed data
│   ├── raw/
│   └── processed/                  # (optional)
│
├── trainer/                        # training / experiment logic
│   ├── __init__.py
│   ├── train.py                    # core training, MLflow logging
│   ├── utils.py                    # helper functions (data loading, preprocessing)
│   └── validation.py               # data validation before training
│
├── model/                          # saved models / artifacts (for deployment)
│
├── serving/                        # inference / API layer
│   ├── __init__.py
│   ├── app.py                       # FastAPI / API endpoints
│   ├── inference.py                 # load model & run prediction logic
│   └── schemas.py                   # Pydantic schemas for requests/responses
│
├── monitoring/                     # metrics / dashboards / integration
│   ├── grafana/
│   ├── prometheus/
│   └── metrics_exporter.py          # code to export metrics
│
└── ci_cd/                           # CI/CD pipeline definitions / scripts
    ├── jenkins/                     # Jenkins pipeline scripts
    └── other_ci/                    # e.g. GitHub Actions if added later
```

### Key design principles / justifications:

1. Separation of concerns

    * trainer/ handles model training logic, logging, experiments.
    * serving/ handles inference, API endpoints, input/output schemas.
    * monitoring/ handles metrics, dashboards, observability.
    * ci_cd/ for pipeline definitions (Jenkins, or future ones).
    * scripts/ for utility scripts (e.g. wait, validation) rather than putting them in root.

2. Modularity

    * You can import trainer.train and use it from CLI or pipeline.
    * serving.inference module can be used independently of FastAPI or integrated into the API.

3. Clear artifact separation

    * mlruns/ for MLflow tracking.
    * model/ for “production models” that are ready for deployment.
    * mlflow/ for server backend storage.

4. Data versioning / structure

  * Keep raw data and processed data separate.
  * Do not commit large data files; use .gitignore or a data versioning tool.

5. CI/CD & MLOps integration

  * Jenkins (in ci_cd/jenkins/) or pipeline scripts to run training, tests, model validation, deployment.
  * The Jenkinsfile can live in the root but reference scripts in ci_cd/jenkins/.

6. Monitoring / Logging

  * Use monitoring/ to integrate metrics exporters, dashboards (Grafana, Prometheus).
  * Keep these separate but integrated via docker-compose or pipeline.

7. Configuration management

   * You might add a config/ folder (or config.yaml) to store hyperparameters, data paths, etc, so they’re not hard-coded.

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
| Jenkins  | http://localhost:5000 |

