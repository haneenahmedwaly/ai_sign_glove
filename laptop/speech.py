
import csv
from pathlib import Path
import pyttsx3

BASE_DIR = Path(__file__).resolve().parent.parent
DICTIONARY_FILE = BASE_DIR / "docs" / "sign_dictionary.csv"

engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    print("Speaking:", text)
    engine.say(text)
    engine.runAndWait()

def get_phrase(sign):
    with open(DICTIONARY_FILE, encoding="utf-8-sig") as file:
        reader = csv.DictReader(file, delimiter="\t")

        for row in reader:
            if row["sign"].strip().lower() == sign.strip().lower():
                return row["english_phrase"]

    return "Sorry, sign not recognized."

if __name__ == "__main__":
    sign = input("Enter recognized sign: ")
    phrase = get_phrase(sign)
    print("English phrase:", phrase)
    speak(phrase)



