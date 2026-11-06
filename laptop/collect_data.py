
import csv
from pathlib import Path
from datetime import datetime

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "real_readings.csv"
SENSOR_COUNT = 10

def collect_reading(session_id):
    print("\n--- AI Sign Language Glove ---")

    label = input("Enter the sign name (example: pain): ").strip()

    if not label:
        print("Sign name cannot be empty.")
        return

    values = []

    for i in range(SENSOR_COUNT):
        while True:
            try:
                value = float(input(f"Sensor {i + 1} reading: "))
                values.append(value)
                break
            except ValueError:
                print("Please enter a number.")

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = DATA_FILE.exists()

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists or DATA_FILE.stat().st_size == 0:
            writer.writerow(
                ["timestamp", "session_id"] +
                [f"sensor_{i}" for i in range(1, SENSOR_COUNT + 1)] +
                ["label"]
            )

        writer.writerow(
            [datetime.now().isoformat(), session_id] + values + [label]
        )

    print("Reading saved successfully!")


if __name__ == "__main__":
    session_id = input("Enter session ID (example: session_01): ").strip()

    if not session_id:
        print("Session ID cannot be empty.")
        raise SystemExit

    while True:
        collect_reading(session_id)

        again = input("\nAdd another reading? (y/n): ").strip().lower()

        if again != "y":
            break

    print("\nData collection finished.")

