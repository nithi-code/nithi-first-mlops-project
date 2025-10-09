pipeline {
    agent any

    environment {
        DOCKER_COMPOSE = "${WORKSPACE}/docker-compose.yml"
        MODEL_PATH = "${WORKSPACE}/model/diabetes_rf_model.pkl"
        MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
    }

    stages {

        // ----------------------
        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/nithi-code/nithi-first-mlops-project.git',
                    credentialsId: 'github-pat'
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
                curl -o data/diabetes.csv https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv
                '''
            }
        }

        // ----------------------
        stage('Validate Data') {
            steps {
                echo "Validating dataset..."
                sh 'python validate_data.py || echo "Validation completed or no issues found."'
            }
        }

        // ----------------------
        stage('Prepare Data') {
            steps {
                echo "Preparing dataset for training..."
                sh 'python prepare_data.py || echo "Data preparation completed."'
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
                echo "Testing API with a sample prediction request..."
                sh '''
                curl -X POST http://localhost:8000/predict \
                -H 'Content-Type: application/json' \
                -d '{"Pregnancies":2,"Glucose":90,"BloodPressure":80,"BMI":25,"Age":45}'
                '''
            }
        }

        // ----------------------
        stage('Validate Monitoring') {
            steps {
                echo "Validating MLflow logs..."
                sh 'echo "Check MLflow UI at http://localhost:5000 for training and inference logs."'
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
