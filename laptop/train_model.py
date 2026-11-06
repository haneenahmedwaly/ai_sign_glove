
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupShuffleSplit
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "test_data" / "real_readings.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_FILE = MODEL_DIR / "sign_model.joblib"

# 1. Check dataset
if not DATA_FILE.exists():
    print("Dataset not found. Collect data first.")
    raise SystemExit

data = pd.read_csv(DATA_FILE)

# 2. Check required columns
sensor_columns = [f"sensor_{i}" for i in range(1, 11)]
required_columns = sensor_columns + ["label", "session_id"]

missing_columns = [
    col for col in required_columns if col not in data.columns
]

if missing_columns:
    print("Missing columns:", missing_columns)
    raise SystemExit

# 3. Clean data
data = data.dropna(subset=required_columns).copy()

data["label"] = data["label"].astype(str).str.strip()
data["session_id"] = data["session_id"].astype(str).str.strip()

data = data[
    (data["label"] != "") &
    (data["label"].str.lower() != "test") &
    (data["session_id"] != "")
].copy()

# 4. Convert sensor readings to numbers
for col in sensor_columns:
    data[col] = pd.to_numeric(data[col], errors="coerce")

data = data.dropna(subset=sensor_columns)

# 5. Check dataset size
if data.empty:
    print("No valid real readings found.")
    raise SystemExit

if data["label"].nunique() < 2:
    print("You need at least TWO different real signs.")
    raise SystemExit

if data["session_id"].nunique() < 2:
    print("You need at least TWO different recording sessions.")
    raise SystemExit

# 6. Prepare data
X = data[sensor_columns]
y = data["label"]
groups = data["session_id"]

# 7. Split by recording session
splitter = GroupShuffleSplit(
    n_splits=20,
    test_size=0.25,
    random_state=42
)

selected_split = None

for train_index, test_index in splitter.split(X, y, groups):
    train_labels = set(y.iloc[train_index])
    test_labels = set(y.iloc[test_index])
    all_labels = set(y)

    if train_labels == all_labels and test_labels == all_labels:
        selected_split = (train_index, test_index)
        break

if selected_split is None:
    print("Cannot create a valid session-based split.")
    print("Collect more sessions for every sign.")
    raise SystemExit

train_index, test_index = selected_split

X_train = X.iloc[train_index]
X_test = X.iloc[test_index]
y_train = y.iloc[train_index]
y_test = y.iloc[test_index]

# 8. Train model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X_train, y_train)

# 9. Evaluate model
predictions = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, predictions))
print("\nClassification Report:")
print(classification_report(
    y_test,
    predictions,
    zero_division=0
))

# 10. Save model
MODEL_DIR.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL_FILE)

print("\nModel saved successfully!")
print("Location:", MODEL_FILE)

