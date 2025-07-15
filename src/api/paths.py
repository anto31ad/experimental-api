import os
from pathlib import Path

DATA_DIR = Path('data')
if not DATA_DIR.exists():
    os.makedirs(DATA_DIR)

DB_DIR = DATA_DIR / Path('db')
if not DB_DIR.exists():
    os.makedirs(DB_DIR)

SERVICES_DB_FILEPATH = DB_DIR / Path('services.json')
