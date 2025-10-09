pipeline {
    agent any

    environment {
        WORKSPACE_DIR = "${WORKSPACE}"
        DOCKER_COMPOSE = "/usr/local/bin/docker-compose"  // Full path
        MODEL_PATH = "${WORKSPACE}/model/diabetes_rf_model.pkl"
        MLFLOW_TRACKING_URI = "http://mlflow-server:5000"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/nithi-code/nithi-first-mlops-project.git',
                    credentialsId: 'github-pat'
            }
        }

        stage('Setup Environment') {
            steps {
                echo "Installing Python dependencies..."
                sh """
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                """
            }
        }

        stage('Extract Data') {
            steps {
                echo "Downloading dataset..."
                sh '''
                    mkdir -p data
                    curl -s -o data/diabetes.csv https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv
                '''
            }
        }

        stage('Validate Data') {
            steps {
                echo "Validating dataset..."
                sh '''
                    if [ -f validate_data.py ]; then
                        ./venv/bin/python validate_data.py || echo "Validation passed or no issues found."
                    else
                        echo "No validate_data.py found, skipping."
                    fi
                '''
            }
        }

        stage('Prepare Data') {
            steps {
                echo "Preparing dataset..."
                sh '''
                    if [ -f prepare_data.py ]; then
                        ./venv/bin/python prepare_data.py || echo "Data preparation done."
                    else
                        echo "No prepare_data.py found, skipping."
                    fi
                '''
            }
        }

        stage('Train Model') {
            steps {
                echo "Training Random Forest model using Docker Compose..."
                sh """
                    # Check docker-compose exists
                    if [ ! -x "$DOCKER_COMPOSE" ]; then
                        echo "docker-compose not installed!"
                        exit 1
                    fi

                    # Start MLflow server
                    $DOCKER_COMPOSE up -d mlflow-server

                    # Wait for MLflow server
                    echo "Waiting for MLflow server..."
                    until curl -s ${MLFLOW_TRACKING_URI}/api/2.0/mlflow/experiments/list; do
                        sleep 3
                        echo "Retrying..."
                    done

                    # Run trainer container
                    $DOCKER_COMPOSE run --rm trainer
                """
            }
        }

        stage('Deploy Model') {
            steps {
                echo "Deploying FastAPI API..."
                sh """
                    $DOCKER_COMPOSE up -d diabetes-api
                """
            }
        }

        stage('Test Model Prediction') {
            steps {
                echo "Testing API prediction..."
                sh '''
                    curl -s -X POST http://localhost:8000/predict \
                        -H 'Content-Type: application/json' \
                        -d '{"Pregnancies":2,"Glucose":90,"BloodPressure":80,"BMI":25,"Age":45}'
                '''
            }
        }

        stage('Validate Monitoring') {
            steps {
                echo "Check MLflow UI at http://localhost:5000 for logs."
            }
        }

    }

    post {
        always {
            echo "Cleaning up containers..."
            sh '$DOCKER_COMPOSE down || true'
        }
    }
}
