import psutil
import GPUtil
import os
import time
from colorama import Fore, Style



last_recv = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent

def color_use(value):
    if value > 80:
        color = Fore.RED
    elif value > 50:
        color = Fore.YELLOW
    else:
        color = Fore.GREEN
    return f"{color}{value}%" + Fore.RESET

def color_temp(value):
    if value > 90:
        color = Fore.RED
    elif value > 70:
        color = Fore.YELLOW
    else:
        color = Fore.GREEN
    return f"{color}{value}°C" + Fore.RESET

def status():
    global last_recv, last_sent
    os.system('cls' if os.name == 'nt' else 'clear')

    print("=== SYSTEM STATUS ===")

    # CPU
    cpusage = psutil.cpu_percent()
    print(f"CPU Usage : {color_use(cpusage)}")

    # Memory 
    ram = psutil.virtual_memory()
    print(f"RAM : {color_use(ram.percent)} ({ram.used // 1024**2} Mo / {ram.total // 1024**2} Mo)")


    # GPU
    gpus = GPUtil.getGPUs()
    if not gpus:
        print(Fore.RED + "GPU: No GPU detected")
    else:
        for gpu in gpus:
            print(f"GPU ({gpu.name}) : {color_use(gpu.load*100)} | Temp : {color_temp(gpu.temperature)}")
    
    print('')

    # Disk
    partitions = psutil.disk_partitions()
    for p in partitions:
        disk = psutil.disk_usage(p.mountpoint)
        print(f"Disk {p.device} Free {disk.free / (1024**3):.2f} GB | Used {disk.used / (1024**3):.2f} GB")

    print('')

    # Network
    actual = psutil.net_io_counters()
    spd_dwnld = actual.bytes_recv - last_recv
    spd_upld = actual.bytes_sent - last_sent
    last_recv = actual.bytes_recv
    last_sent = actual.bytes_sent
    print(f"Download speed : {spd_dwnld / (1024):.2f} kB/s")
    print(f"Upload speed : {spd_upld / (1024):.2f} kB/s")
    
    print("=====================")

try:
    while True:
        status()
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\nExiting...")