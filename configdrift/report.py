import json
from pathlib import Path

def export_json(diffs, path):
    with open(path, 'w') as f:
        json.dump(diffs, f, indent=2)

def export_text(diffs, path):
    with open(path, 'w') as f:
        for file, diff in diffs.items():
            f.write(f'==== {file} ====' + '\n')
            for op, data in diff:
                f.write(f'{op}: {data}\n')
            f.write('\n')

def export_html(diffs, path):
    with open(path, 'w') as f:
        f.write('<html><body>')
        for file, diff in diffs.items():
            f.write(f'<h2>{file}</h2><pre>')
            for op, data in diff:
                color = 'black'
                if op == 0:
                    color = 'black'
                elif op == -1 or op == 'REMOVED':
                    color = 'red'
                elif op == 1 or op == 'ADDED':
                    color = 'green'
                f.write(f'<span style="color:{color}">{op}: {data}</span>\n')
            f.write('</pre>')
        f.write('</body></html>') 