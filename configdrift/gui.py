from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QTabWidget, QPushButton, QLineEdit, QTextEdit, QListWidget, QFileDialog, QMessageBox, QHBoxLayout, QComboBox
)
from PyQt5.QtCore import Qt
from . import baseline, collector, detector, diffview, report
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Configuration Drift Detector')
        self.resize(800, 600)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.init_home()
        self.init_baseline()
        self.init_detect()
        self.init_export()
        self.init_settings()

    def init_home(self):
        home = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<h2>Welcome to the Configuration Drift Detector GUI!</h2>'))
        layout.addWidget(QLabel('Use the tabs to manage baselines, detect drift, and export reports.'))
        home.setLayout(layout)
        self.tabs.addTab(home, 'Home')

    def init_baseline(self):
        tab = QWidget()
        layout = QVBoxLayout()
        self.baseline_list = QListWidget()
        self.refresh_baselines()
        layout.addWidget(QLabel('<b>Baselines:</b>'))
        layout.addWidget(self.baseline_list)
        btn_refresh = QPushButton('Refresh List')
        btn_refresh.clicked.connect(self.refresh_baselines)
        layout.addWidget(btn_refresh)
        layout.addWidget(QLabel('Create/Update Baseline:'))
        self.base_name = QLineEdit()
        self.base_name.setPlaceholderText('Baseline name')
        layout.addWidget(self.base_name)
        self.preset_box = QComboBox()
        self.preset_box.addItems(['', 'windows', 'linux', 'mac'])
        layout.addWidget(self.preset_box)
        self.paths_edit = QLineEdit()
        self.paths_edit.setPlaceholderText('Additional paths (comma separated)')
        layout.addWidget(self.paths_edit)
        btn_create = QPushButton('Create Baseline')
        btn_create.clicked.connect(self.create_baseline)
        layout.addWidget(btn_create)
        btn_update = QPushButton('Update Baseline')
        btn_update.clicked.connect(self.update_baseline)
        layout.addWidget(btn_update)
        btn_show = QPushButton('Show Selected Baseline')
        btn_show.clicked.connect(self.show_baseline)
        layout.addWidget(btn_show)
        self.baseline_content = QTextEdit()
        self.baseline_content.setReadOnly(True)
        layout.addWidget(self.baseline_content)
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Baselines')

    def refresh_baselines(self):
        self.baseline_list.clear()
        for b in baseline.list_baselines():
            self.baseline_list.addItem(b)

    def create_baseline(self):
        name = self.base_name.text().strip()
        preset = self.preset_box.currentText() or None
        paths = [p.strip() for p in self.paths_edit.text().split(',') if p.strip()]
        data = collector.collect_configs(paths=paths, preset=preset)
        baseline.save_baseline(name, data)
        QMessageBox.information(self, 'Success', f'Baseline "{name}" saved.')
        self.refresh_baselines()

    def update_baseline(self):
        name = self.base_name.text().strip()
        preset = self.preset_box.currentText() or None
        paths = [p.strip() for p in self.paths_edit.text().split(',') if p.strip()]
        data = collector.collect_configs(paths=paths, preset=preset)
        baseline.update_baseline(name, data)
        QMessageBox.information(self, 'Success', f'Baseline "{name}" updated.')
        self.refresh_baselines()

    def show_baseline(self):
        items = self.baseline_list.selectedItems()
        if not items:
            QMessageBox.warning(self, 'Error', 'No baseline selected.')
            return
        name = items[0].text()
        try:
            data = baseline.load_baseline(name)
            text = ''
            for path, content in data.items():
                text += f'==== {path} ====' + os.linesep + content + os.linesep
            self.baseline_content.setPlainText(text)
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def init_detect(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<b>Detect Drift:</b>'))
        self.detect_base_box = QComboBox()
        self.detect_base_box.addItems([''] + baseline.list_baselines())
        layout.addWidget(self.detect_base_box)
        self.detect_preset = QComboBox()
        self.detect_preset.addItems(['', 'windows', 'linux', 'mac'])
        layout.addWidget(self.detect_preset)
        self.detect_paths = QLineEdit()
        self.detect_paths.setPlaceholderText('Additional paths (comma separated)')
        layout.addWidget(self.detect_paths)
        btn_detect = QPushButton('Detect Drift')
        btn_detect.clicked.connect(self.run_detect)
        layout.addWidget(btn_detect)
        self.detect_result = QTextEdit()
        self.detect_result.setReadOnly(True)
        layout.addWidget(self.detect_result)
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Detect Drift')

    def run_detect(self):
        name = self.detect_base_box.currentText().strip()
        preset = self.detect_preset.currentText() or None
        paths = [p.strip() for p in self.detect_paths.text().split(',') if p.strip()]
        try:
            base = baseline.load_baseline(name)
            current = collector.collect_configs(paths=paths, preset=preset)
            diffs = detector.detect_drift(current, base)
            if not diffs:
                self.detect_result.setPlainText('No drift detected.')
                return
            text = ''
            for path, diff in diffs.items():
                text += f'==== {path} ====' + os.linesep
                for op, data in diff:
                    if op == 0:
                        text += data + os.linesep
                    elif op == -1 or op == "REMOVED":
                        text += f'- {data}' + os.linesep
                    elif op == 1 or op == "ADDED":
                        text += f'+ {data}' + os.linesep
            self.detect_result.setPlainText(text)
        except Exception as e:
            self.detect_result.setPlainText(f'Error: {e}')

    def init_export(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<b>Export Drift Report:</b>'))
        self.export_base_box = QComboBox()
        self.export_base_box.addItems([''] + baseline.list_baselines())
        layout.addWidget(self.export_base_box)
        self.export_format = QComboBox()
        self.export_format.addItems(['json', 'html', 'text'])
        layout.addWidget(self.export_format)
        self.export_out = QLineEdit()
        self.export_out.setPlaceholderText('Output file path')
        layout.addWidget(self.export_out)
        btn_export = QPushButton('Export Report')
        btn_export.clicked.connect(self.run_export)
        layout.addWidget(btn_export)
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Export')

    def run_export(self):
        name = self.export_base_box.currentText().strip()
        fmt = self.export_format.currentText()
        out = self.export_out.text().strip()
        preset = None
        paths = []
        try:
            base = baseline.load_baseline(name)
            current = collector.collect_configs(paths=paths, preset=preset)
            diffs = detector.detect_drift(current, base)
            if not diffs:
                QMessageBox.information(self, 'Export', 'No drift detected.')
                return
            if fmt == 'json':
                report.export_json(diffs, out)
            elif fmt == 'html':
                report.export_html(diffs, out)
            elif fmt == 'text':
                report.export_text(diffs, out)
            QMessageBox.information(self, 'Export', f'Report exported to {out}.')
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))

    def init_settings(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QLabel('<b>Settings & Help</b>'))
        btn_sched = QPushButton('Show Scheduling Instructions')
        btn_sched.clicked.connect(self.show_sched)
        layout.addWidget(btn_sched)
        btn_notify = QPushButton('Test Notification')
        btn_notify.clicked.connect(self.test_notify)
        layout.addWidget(btn_notify)
        btn_email = QPushButton('Email Notification Instructions')
        btn_email.clicked.connect(self.email_instructions)
        layout.addWidget(btn_email)
        tab.setLayout(layout)
        self.tabs.addTab(tab, 'Settings')

    def show_sched(self):
        import io
        import contextlib
        from . import scheduler
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            scheduler.print_schedule_instructions()
        QMessageBox.information(self, 'Scheduling', buf.getvalue())

    def test_notify(self):
        from . import notify
        notify.notify_user('This is a test notification from ConfigDrift.')

    def email_instructions(self):
        from . import notify
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            notify.print_email_instructions()
        QMessageBox.information(self, 'Email Instructions', buf.getvalue()) 