import pandas as pd
import sys

DATA_PATH = "data/diabetes.csv"

try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"Dataset not found at {DATA_PATH}")
    sys.exit(1)

# Check required columns
required_cols = ["Pregnancies", "Glucose", "BloodPressure", "BMI", "Age", "Outcome"]
missing_cols = [c for c in required_cols if c not in df.columns]
if missing_cols:
    print(f"Missing required columns: {missing_cols}")
    sys.exit(1)

# Check for missing values
if df[required_cols].isnull().sum().sum() > 0:
    print("Warning: Missing values detected in dataset")
else:
    print("Data validation passed: all required columns exist and no missing values.")
