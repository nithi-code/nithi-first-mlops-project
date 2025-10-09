import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score
import mlflow

# ==== Config ====
DATA_URL = "https://raw.githubusercontent.com/plotly/datasets/master/diabetes.csv"
MODEL_PATH = "model/diabetes_rf_model.pkl"
EXPERIMENT_NAME = "Diabetes-Prediction-Training"

# ==== Create folders if missing ====
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

# ==== Load dataset ====
df = pd.read_csv(DATA_URL)

# Use selected features
X = df[["Pregnancies", "Glucose", "BloodPressure", "BMI", "Age"]]
y = df["Outcome"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Hyperparameters
n_estimators = 100
max_depth = 5

# ==== MLflow experiment ====
mlflow.set_experiment(EXPERIMENT_NAME)

with mlflow.start_run(run_name="diabetes_rf_training"):
    # Initialize and train model
    model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)
    model.fit(X_train, y_train)

    # Predictions
    y_pred = model.predict(X_test)

    # Metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    acc = accuracy_score(y_test, y_pred)

    # Log parameters
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)

    # Log metrics
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("accuracy", acc)

    # Log model artifact
    joblib.dump(model, MODEL_PATH)
    mlflow.log_artifact(MODEL_PATH, artifact_path="model")

    print(f"Model saved to {MODEL_PATH}")
    print(f"MSE: {mse:.4f}, R2: {r2:.4f}, Accuracy: {acc:.4f}")
