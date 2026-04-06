import psutil
import GPUtil
import os
import time
import datetime
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

# Bars
def make_bar(percent, length=20):
    filled_length = int(length * percent // 100)
    
    bar = '█' * filled_length + '-' * (length - filled_length)
    
    return f"[{bar}]"

# Processes fuction
def get_top_proc():
    processes = []

    psutil.cpu_percent(interval=None) 
    
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
        try:
            cpu = proc.info['cpu_percent']
            name = proc.info['name']
            ramMB = proc.info['memory_info'].rss // 1024**2

            if name == "System Idle Process" or name is None:
                continue
                
            processes.append({
                'name': name, 
                'cpu': round(cpu / cores, 2),
                'ram': ramMB
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    top3_cpu = sorted(processes, key=lambda x: x['cpu'], reverse=True)[:3]
    top3_ram = sorted(processes, key=lambda x: x['ram'], reverse=True)[:3]
    return top3_cpu, top3_ram

# Main function
def status():
    global last_recv, last_sent
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"=== SYSTEM STATUS ===")

    # Uptime
    boot_time = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    print(f"Uptime : {str(uptime).split('.')[0]}")

    # CPU
    cpusage = psutil.cpu_percent()
    cpu_bar = make_bar(cpusage)
    print(f"CPU Usage : {cpu_bar} {color_use(cpusage)}")

    # Memory 
    ram = psutil.virtual_memory()
    ram_bar = make_bar(ram.percent)
    print(f"RAM       : {ram_bar} {color_use(ram.percent)}")
    
    swram = psutil.swap_memory()
    print(f'Virtual RAM : {color_use(swram.percent)} ({swram.used // 1024**2} MB / {swram.total // 1024**2} MB)')


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
    
    # Inside status()
    cpu_list, ram_list = get_top_proc()

    print(f"{'--- TOP CPU ---':<30} | {'--- TOP RAM ---':<30}")

    # Iterate through both lists using zip
    for c, r in zip(cpu_list, ram_list):
        cpu_name = c['name'][:15].ljust(15)
        cpu_val = color_use(c['cpu'])
        left_col = f"{cpu_name} : {cpu_val}"

        ram_name = r['name'][:15].ljust(15)
        ram_val = f"{r['ram']} Mo"
        right_col = f"{ram_name} : {ram_val}"

        print(f"{left_col:<40} | {right_col}")
        
    print("=====================")

try:
    while True:
        status()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")