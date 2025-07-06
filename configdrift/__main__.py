import sys
import click
from rich.console import Console
from . import baseline, collector, detector, diffview, report, notify, scheduler

console = Console()

def launch_gui():
    try:
        from PyQt5.QtWidgets import QApplication
        from .gui import MainWindow
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except ImportError:
        console.print('[red]PyQt5 is not installed. Please install it to use the GUI.[/red]')

@click.group()
def main():
    """Configuration Drift Detector CLI/GUI"""
    pass

@main.command()
@click.option('--name', prompt='Baseline name', help='Name for the new baseline')
@click.option('--preset', default=None, help='Preset to use (windows/linux/mac)')
@click.option('--paths', multiple=True, help='Additional config file paths')
def create_baseline(name, preset, paths):
    """Create a new baseline from current configs."""
    data = collector.collect_configs(paths=paths, preset=preset)
    baseline.save_baseline(name, data)
    console.print(f'[green]Baseline "{name}" saved with {len(data)} files.[/green]')

@main.command()
def list_baselines():
    """List all baselines."""
    bls = baseline.list_baselines()
    if not bls:
        console.print('[yellow]No baselines found.[/yellow]')
    else:
        for b in bls:
            console.print(f'- {b}')

@main.command()
@click.argument('name')
def show_baseline(name):
    """Show contents of a baseline."""
    try:
        data = baseline.load_baseline(name)
        for path, content in data.items():
            console.rule(f'[bold blue]{path}')
            console.print(content)
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@main.command()
@click.argument('name')
@click.option('--preset', default=None, help='Preset to use (windows/linux/mac)')
@click.option('--paths', multiple=True, help='Additional config file paths')
def update_baseline(name, preset, paths):
    """Update an existing baseline with current configs."""
    data = collector.collect_configs(paths=paths, preset=preset)
    baseline.update_baseline(name, data)
    console.print(f'[green]Baseline "{name}" updated.[/green]')

@main.command()
@click.argument('name')
@click.option('--preset', default=None, help='Preset to use (windows/linux/mac)')
@click.option('--paths', multiple=True, help='Additional config file paths')
@click.option('--export', type=click.Choice(['json', 'html', 'text']), default=None, help='Export report format')
@click.option('--out', default=None, help='Output file for export')
@click.option('--notify', is_flag=True, help='Send notification if drift detected')
def detect(name, preset, paths, export, out, notify):
    """Detect configuration drift against a baseline."""
    try:
        base = baseline.load_baseline(name)
        current = collector.collect_configs(paths=paths, preset=preset)
        diffs = detector.detect_drift(current, base)
        if not diffs:
            console.print('[green]No drift detected.[/green]')
            return
        diffview.print_diff(diffs)
        if export and out:
            if export == 'json':
                report.export_json(diffs, out)
            elif export == 'html':
                report.export_html(diffs, out)
            elif export == 'text':
                report.export_text(diffs, out)
            console.print(f'[green]Report exported to {out}.[/green]')
        if notify:
            notify.notify_user(f'Drift detected for baseline {name}!')
    except Exception as e:
        console.print(f'[red]Error: {e}[/red]')

@main.command()
def schedule():
    """Print instructions for scheduling drift checks."""
    scheduler.print_schedule_instructions()

@main.command()
def test_notify():
    """Test desktop notification."""
    notify.notify_user('This is a test notification from ConfigDrift.')

@main.command()
def email_instructions():
    """Print instructions for email notifications."""
    notify.print_email_instructions()

@main.command()
def gui():
    """Launch the GUI interface."""
    launch_gui()

if __name__ == '__main__':
    main() 