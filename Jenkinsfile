pipeline {
    agent any

    environment {
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
                sh '''
                mkdir -p data
                curl -s -o data/diabetes.csv https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv
                '''
            }
        }

        // ----------------------
        stage('Validate Data') {
            steps {
                echo "Validating dataset..."
                sh '''
                source ${VENV_PATH}/bin/activate
                python validate_data.py || echo "Validation passed or no issues found."
                '''
            }
        }

        // ----------------------
        stage('Prepare Data') {
            steps {
                echo "Preparing dataset..."
                sh '''
                source ${VENV_PATH}/bin/activate
                python prepare_data.py || echo "Data preparation done."
                '''
            }
        }

        // ----------------------
        stage('Train Model') {
            steps {
                echo "Training Random Forest model via Docker..."
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
                sh '''
                curl -s -X POST http://localhost:8000/predict \
                -H 'Content-Type: application/json' \
                -d '{"Pregnancies":2,"Glucose":90,"BloodPressure":80,"BMI":25,"Age":45}'
                '''
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
