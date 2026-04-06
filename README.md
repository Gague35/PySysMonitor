# 🚀 PySysMonitor

A lightweight, real-time system resource monitor built with Python. This tool provides instant visibility into your machine's performance directly from your terminal with dynamic color-coding.

## 📊 Features
* **CPU Monitoring**: Real-time load percentage with dynamic color-coding (Green/Yellow/Red).
* **Memory (RAM)**: Track usage percentages and precise data (Used vs. Total in MB).
* **GPU Tracking**: Automatic detection of NVIDIA graphics cards, showing both load and temperature.
* **Disk Analysis**: Dynamic monitoring of all detected partitions (C:, D:, F:, etc.) with free and used space and dynamic color (Cyan/Red)
* **Network Traffic**: Live calculation of Download and Upload speeds in kB/s.

## 🛠️ Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Gague35/PySysMonitor.git
    ```

2. **Install the required dependencies**:
    ```bash
    pip install psutil gputil colorama distutils
    ```

## 🚀 How to Use

Simply run the main script:

```bash
python main.py
```

*To exit the monitor, press Ctrl + C in your terminal.*

## 📅 Roadmap (Future Updates)
- [ ] **Advanced Hardware Data**: CPU per-core temperatures and fan speeds.
- [ ] **Process Tracking**: Displaying the "Top 3" most resource-hungry applications.
- [ ] **Session History**: Tracking peak (Max/Min) values during the monitoring session.
- [ ] **Dedicated GUI**: Transitioning from a CLI to a full standalone desktop application.

## 📚 Libraries Used
* **[psutil](https://github.com/giampaolo/psutil)**: Used for retrieving information on running processes and system utilization (CPU, memory, disks, network).
* **[GPUtil](https://github.com/anderskm/gputil)**: A Python module for getting the GPU status from NVIDIA GPUs using nvidia-smi.
* **[colorama](https://github.com/tartley/colorama)**: Simple cross-platform colored terminal text in Python.