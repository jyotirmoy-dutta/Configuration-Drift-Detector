import os
import tempfile
from pathlib import Path
from configdrift import baseline, collector, detector, diffview, report

def test_baseline_save_load_list():
    with tempfile.TemporaryDirectory() as tmp:
        baseline.BASELINE_DIR = Path(tmp)
        data = {'/etc/hosts': '127.0.0.1'}
        baseline.save_baseline('test', data)
        assert 'test' in baseline.list_baselines()
        loaded = baseline.load_baseline('test')
        assert loaded == data

def test_collector():
    with tempfile.NamedTemporaryFile('w+', delete=False) as f:
        f.write('test content')
        f.flush()
        data = collector.collect_configs(paths=[f.name])
        assert f.name in data
        assert data[f.name] == 'test content'
    os.unlink(f.name)

def test_detector():
    base = {'a': 'foo\nbar'}
    curr = {'a': 'foo\nbaz'}
    diffs = detector.detect_drift(curr, base)
    assert 'a' in diffs
    # Reconstruct the new string from the diff
    reconstructed = ''
    for op, data in diffs['a']:
        if op != -1:  # not a deletion
            reconstructed += data
    assert reconstructed == curr['a']

def test_report(tmp_path):
    diffs = {'a': [(0, 'foo'), (1, 'bar'), (-1, 'baz')]}
    json_path = tmp_path / 'out.json'
    text_path = tmp_path / 'out.txt'
    html_path = tmp_path / 'out.html'
    report.export_json(diffs, json_path)
    report.export_text(diffs, text_path)
    report.export_html(diffs, html_path)
    assert json_path.exists() and text_path.exists() and html_path.exists()

def test_plugin_loading():
    import importlib
    plugin = importlib.import_module('configdrift.plugins.sample_plugin')
    assert hasattr(plugin, 'run') 