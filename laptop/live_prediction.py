
from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "models" / "sign_model.joblib"

SENSOR_COLUMNS = [f"sensor_{i}" for i in range(1, 11)]

def predict_sign(readings):
    if len(readings) != 10:
        raise ValueError("Exactly 10 sensor readings are required.")

    model = joblib.load(MODEL_FILE)

    data = pd.DataFrame([readings], columns=SENSOR_COLUMNS)

    prediction = model.predict(data)[0]

    print("Predicted sign:", prediction)

    return prediction


if __name__ == "__main__":
    if not MODEL_FILE.exists():
        print("AI model not trained yet.")
    else:
        readings = []

        for i in range(10):
            value = float(input(f"Enter sensor {i + 1}: "))
            readings.append(value)

        predict_sign(readings)
