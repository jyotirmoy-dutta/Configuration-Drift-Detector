import os
import json
from pathlib import Path

BASELINE_DIR = Path.home() / '.configdrift' / 'baselines'
BASELINE_DIR.mkdir(parents=True, exist_ok=True)

def save_baseline(name, data):
    with open(BASELINE_DIR / f'{name}.json', 'w') as f:
        json.dump(data, f, indent=2)

def load_baseline(name):
    with open(BASELINE_DIR / f'{name}.json') as f:
        return json.load(f)

def list_baselines():
    return [f.stem for f in BASELINE_DIR.glob('*.json')]

def update_baseline(name, data):
    save_baseline(name, data) 