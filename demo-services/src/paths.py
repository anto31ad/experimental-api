import os
from pathlib import Path

DATA_DIR = Path('data')
if not DATA_DIR.exists():
    os.makedirs(DATA_DIR)

MODELS_DIR = DATA_DIR / Path('models')
if not MODELS_DIR.exists():
    os.makedirs(MODELS_DIR)

IRIS_MODEL_FILEPATH = MODELS_DIR / Path('iris_classifier.pkl')
DIGITS_MODEL_FILEPATH = MODELS_DIR / Path('digit_classifier.pkl')
DIGITS_EXAMPLE_FILEPATH = DATA_DIR / Path('digit_example.json')
