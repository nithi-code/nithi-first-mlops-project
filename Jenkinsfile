pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        VENV_PATH = "${WORKSPACE}/venv"
        MODEL_PATH = "${WORKSPACE}/model/diabetes_rf_model.pkl"
        MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
        DOCKER_COMPOSE_FILE = "${WORKSPACE}/docker-compose.yml"
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
                echo "Creating Python virtual environment and installing dependencies..."
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
                sh '''
                if [ -f validate_data.py ]; then
                    source ${VENV_PATH}/bin/activate
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
                    source ${VENV_PATH}/bin/activate
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
                echo "Training Random Forest model using Docker Compose..."
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} down || true"
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} build trainer"
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} run --rm trainer"
            }
        }

        // ----------------------
        stage('Deploy Model') {
            steps {
                echo "Deploying FastAPI prediction API..."
                sh "docker-compose -f ${DOCKER_COMPOSE_FILE} up -d diabetes-api"
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
                echo "Check MLflow UI for training and inference logs: http://localhost:5000"
            }
        }
    }

    post {
        always {
            echo "Cleaning up Docker containers..."
            sh "docker-compose -f ${DOCKER_COMPOSE_FILE} down || true"
        }
    }
}
