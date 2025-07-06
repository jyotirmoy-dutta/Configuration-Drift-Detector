from rich.console import Console
from rich.text import Text

console = Console()

def print_diff(diffs):
    for path, diff in diffs.items():
        console.rule(f"[bold blue]{path}")
        for op, data in diff:
            if op == 0:
                console.print(data, style="white")
            elif op == -1 or op == 'REMOVED':
                console.print(data, style="red")
            elif op == 1 or op == 'ADDED':
                console.print(data, style="green") 