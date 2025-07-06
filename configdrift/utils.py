import platform
import os
from pathlib import Path

def get_os_name():
    return platform.system().lower()

def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True) 