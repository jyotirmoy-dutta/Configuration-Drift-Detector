import os
from pathlib import Path

PRESETS = {
    'windows': [r'C:\Windows\System32\drivers\etc\hosts'],
    'linux': ['/etc/hosts', '/etc/passwd'],
    'mac': ['/etc/hosts', '/etc/passwd'],
}

def collect_configs(paths=None, preset=None):
    files = []
    if preset:
        files.extend(PRESETS.get(preset, []))
    if paths:
        files.extend(paths)
    collected = {}
    for path in files:
        p = Path(path)
        if p.exists():
            with open(p, 'r', errors='ignore') as f:
                collected[str(p)] = f.read()
    return collected 