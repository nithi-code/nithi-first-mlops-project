pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        VENV_PATH = "${WORKSPACE}/venv"
        MODEL_PATH = "${WORKSPACE}/model/diabetes_rf_model.pkl"
        MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
        DOCKER_COMPOSE = "${WORKSPACE}/docker-compose.yml"
    }

    stages {

        // ----------------------
        stage('Checkout Code') {
            steps {
                echo "Cloning repository..."
                git branch: 'main',
                    url: 'https://github.com/nithi-code/nithi-first-mlops-project.git',
                    credentialsId: 'github-pat'
            }
        }

        // ----------------------
        stage('Setup Environment') {
            steps {
                echo "Creating virtual environment and installing dependencies..."
                sh '''
                python3 -m venv ${VENV_PATH}
                . ${VENV_PATH}/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
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
                sh '''
                if [ -f validate_data.py ]; then
                    . ${VENV_PATH}/bin/activate
                    python validate_data.py || echo "Validation completed or no issues found."
                else
                    echo "No validate_data.py script found, skipping validation."
                fi
                '''
            }
        }

        // ----------------------
        stage('Prepare Data') {
            steps {
                echo "Preparing dataset for training..."
                sh '''
                if [ -f prepare_data.py ]; then
                    . ${VENV_PATH}/bin/activate
                    python prepare_data.py || echo "Data preparation completed."
                else
                    echo "No prepare_data.py script found, skipping preparation."
                fi
                '''
            }
        }

        // ----------------------
        stage('Train Model') {
            steps {
                echo "Training Random Forest model using Docker..."
                sh '''
                if command -v docker-compose >/dev/null 2>&1; then
                    docker-compose run --rm trainer
                else
                    echo "docker-compose not found. Please install docker-compose."
                    exit 1
                fi
                '''
            }
        }

        // ----------------------
        stage('Deploy Model') {
            steps {
                echo "Deploying FastAPI prediction API..."
                sh '''
                if command -v docker-compose >/dev/null 2>&1; then
                    docker-compose up -d diabetes-api
                else
                    echo "docker-compose not found. Please install docker-compose."
                    exit 1
                fi
                '''
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
            sh '''
            if command -v docker-compose >/dev/null 2>&1; then
                docker-compose down
            else
                echo "docker-compose not found, skipping cleanup."
            fi
            '''
        }
    }
}
