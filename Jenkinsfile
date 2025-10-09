pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        DOCKER_COMPOSE = "${WORKSPACE}/docker-compose.yml"
        MODEL_PATH = "${WORKSPACE}/model/diabetes_rf_model.pkl"
        MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
        VENV_PATH = "${WORKSPACE}/venv"
    }

    stages {

        // ----------------------
        stage('Checkout Code') {
            steps {
                echo "Cloning repository..."
                git branch: 'main',
                    url: 'https://github.com/nithi-code/nithi-first-mlops-project.git'
            }
        }

        // ----------------------
        stage('Setup Environment') {
            steps {
                echo "Creating virtual environment and installing dependencies..."
                sh """
                    python3 -m venv ${VENV_PATH}
                    ${VENV_PATH}/bin/pip install --upgrade pip
                    ${VENV_PATH}/bin/pip install -r requirements.txt
                """
            }
        }

        // ----------------------
        stage('Extract Data') {
            steps {
                echo "Downloading dataset..."
                sh """
                mkdir -p data
                curl -s -o data/diabetes.csv https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv
                """
            }
        }

        // ----------------------
        stage('Validate Data') {
            steps {
                echo "Validating dataset..."
                sh """
                ${VENV_PATH}/bin/python - << 'EOF'
import pandas as pd
import sys

DATA_PATH = "data/diabetes.csv"

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Dataset not found at {DATA_PATH}")
    sys.exit(1)

required_cols = ["Pregnancies", "Glucose", "BloodPressure", "BMI", "Age", "Outcome"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    print(f"Missing required columns: {missing_cols}")
    sys.exit(1)

if df[required_cols].isnull().sum().sum() > 0:
    print("Warning: Missing values detected in dataset")
else:
    print("Data validation passed: all required columns exist and no missing values.")
EOF
                """
            }
        }

        // ----------------------
        stage('Prepare Data') {
            steps {
                echo "Preparing dataset for training..."
            }
        }

        // ----------------------
        stage('Train Model') {
            steps {
                echo "Training Random Forest model using Docker..."
                sh 'docker compose run --rm trainer'
            }
        }

        // ----------------------
        stage('Deploy Model') {
            steps {
                echo "Deploying FastAPI prediction API..."
                sh 'docker compose up -d diabetes-api'
            }
        }

        // ----------------------
        stage('Test Model Prediction') {
            steps {
                echo "Testing API with sample request..."
                sh """
                curl -s -X POST http://localhost:8000/predict \
                -H 'Content-Type: application/json' \
                -d '{"Pregnancies":2,"Glucose":90,"BloodPressure":80,"BMI":25,"Age":45}'
                """
            }
        }

        // ----------------------
        stage('Validate Monitoring') {
            steps {
                echo "Check MLflow logs for training and inference metrics..."
                sh 'echo "Open MLflow UI at http://localhost:5000"'
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker containers..."
            sh 'docker compose down'
        }
    }
}
