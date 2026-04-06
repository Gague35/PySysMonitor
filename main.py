import psutil
import GPUtil
import os
import time
from colorama import Fore

last_recv = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent

cores = psutil.cpu_count()

# Color functions
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

def color_disk(text, percent):
    if percent > 90:
        color = Fore.RED
    else:
        color = Fore.CYAN
    return f"{color}{text}" + Fore.RESET

# Processes fuction
def get_top_proc():
    processes = []

    psutil.cpu_percent(interval=None) 
    
    for proc in psutil.process_iter(['name', 'cpu_percent']):
        try:
            cpu = proc.info['cpu_percent']
            name = proc.info['name']
            
            if name == "System Idle Process" or name is None:
                continue
                
            processes.append({
                'name': name, 
                'cpu': round(cpu / cores, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top3 = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:3]
    return top3

# Main function
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
        try:
            usage = psutil.disk_usage(p.mountpoint)
            free_text = f"{usage.free / (1024**3):.2f} GB"
            used_text = f"{usage.used / (1024**3):.2f} GB"
            
            colored_free = color_disk(free_text, usage.percent)
            colored_used = color_disk(used_text, usage.percent)
            
            print(f"Disk {p.device} Free {colored_free} | Used {colored_used}")
        except PermissionError:
            continue

    print('')

    # Network
    actual = psutil.net_io_counters()
    spd_dwnld = actual.bytes_recv - last_recv
    spd_upld = actual.bytes_sent - last_sent
    last_recv = actual.bytes_recv
    last_sent = actual.bytes_sent
    print(f"Download speed : {spd_dwnld / (1024):.2f} kB/s")
    print(f"Upload speed : {spd_upld / (1024):.2f} kB/s")
    
# Top Processes
    print("--- Top 3 Processes ---")
    top_list = get_top_proc()
    
    for p in top_list:
        print(f"{p['name'][:20]:<20} : {color_use(p['cpu'])}")

    print("=====================")

try:
    while True:
        status()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")