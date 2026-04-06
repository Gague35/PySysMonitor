import psutil
import GPUtil
import os
import time

def status():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=== SYSTEM STATUS ===")

    # CPU
    print(f"CPU Usage: {psutil.cpu_percent()}%")

    # Memory 
    ram = psutil.virtual_memory()
    print(f"RAM : {ram.percent}% ({ram.used // 1024**2} Mo / {ram.total // 1024**2} Mo)")

    # GPU
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("GPU: No GPU detected")
    for gpu in gpus:
        print(f"GPU ({gpu.name}) : {gpu.load*100}% | Temp: {gpu.temperature}°C")
    
    print('')

    # Disk
    partitions = psutil.disk_partitions()
    for p in partitions:
        disk = psutil.disk_usage(p.mountpoint)
        print(f"Disk {p.device} Free {disk.free / (1024**3):.2f} GB | Used {disk.used / (1024**3):.2f} GB")

    # Network
    print(f"Network : {psutil.net_io_counters}")
    
    print("=====================")

try:
    while True:
        status()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExiting...")