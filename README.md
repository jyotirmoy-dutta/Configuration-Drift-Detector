# Configuration Drift Detector

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

> **A robust, professional, cross-platform tool to detect configuration drift by comparing current system/application configs with a golden baseline. Provides both CLI and GUI interfaces.**

---

## 🚀 Features
- **Baseline Management**: Save, update, and manage golden baselines
- **Config Collection**: System & app configs, user-selectable, with OS presets
- **Drift Detection**: Compare current configs to baseline, clear color-coded diff
- **Diff Viewer**: Beautiful CLI output, GUI diff view
- **Exportable Reports**: HTML, JSON, and plain text
- **Scheduling**: OS-native scheduling instructions
- **Notifications**: Desktop notifications (cross-platform)
- **Plugin System**: Easily extend with your own plugins
- **Cross-Platform**: Windows, macOS, Linux
- **100% Local**: No data leaves your machine

---

## 🏗️ Architecture
- **Python 3.8+**
- CLI: [Click](https://click.palletsprojects.com/), [Rich](https://rich.readthedocs.io/)
- GUI: [PyQt5](https://riverbankcomputing.com/software/pyqt/intro)
- Diff: [diff-match-patch](https://github.com/google/diff-match-patch)
- Extensible via plugins

---

## ⚡ Installation
```sh
# Clone the repo
https://github.com/yourusername/configdrift.git
cd configdrift

# Install dependencies
pip install -r requirements.txt
```

---

## 🖥️ CLI Usage
- **Create a baseline:**
  ```sh
  python -m configdrift create-baseline --name mybase --preset windows
  ```
- **List baselines:**
  ```sh
  python -m configdrift list-baselines
  ```
- **Show a baseline:**
  ```sh
  python -m configdrift show-baseline mybase
  ```
- **Update a baseline:**
  ```sh
  python -m configdrift update-baseline mybase --preset windows
  ```
- **Detect drift:**
  ```sh
  python -m configdrift detect mybase --preset windows --export html --out drift.html --notify
  ```
- **Launch the GUI:**
  ```sh
  python -m configdrift gui
  ```
- **Print scheduling instructions:**
  ```sh
  python -m configdrift schedule
  ```
- **Test notification:**
  ```sh
  python -m configdrift test-notify
  ```

---

## 🖱️ GUI Usage
- Launch with:
  ```sh
  python -m configdrift gui
  ```
- Use tabs to manage baselines, detect drift, and export reports.

---

## 🔌 Plugin Development
- Place plugins in `configdrift/plugins/`.
- Each plugin should have a `run()` function.
- Example:
  ```python
  # configdrift/plugins/my_plugin.py
  def run():
      print("My plugin logic!")
  ```
- Load and use plugins via importlib in your own scripts.

---

## 🤝 Contributing
1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## ❓ FAQ
- **Where are baselines stored?**
  - In `~/.configdrift/baselines/` as JSON files.
- **Does this send data to the cloud?**
  - No, all operations are local.
- **How do I schedule checks?**
  - Use the `schedule` command for OS-specific instructions.
- **How do I get notifications?**
  - Desktop notifications are built-in; email support is planned.
- **How do I contribute?**
  - Fork the repo, add features or plugins, and submit a PR!
- **How do I package this as an executable?**
  - Use [PyInstaller](https://pyinstaller.org/) for standalone builds.

---
