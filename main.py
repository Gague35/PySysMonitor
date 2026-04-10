import psutil
import GPUtil
import os
import subprocess
import platform
import cpuinfo
import time
import datetime
from colorama import Fore


last_recv = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent

get_os = platform.system()
get_os_ver = (f'{platform.release()} | Version: {platform.version()}')
cores = psutil.cpu_count()
cpu_name = cpuinfo.get_cpu_info()["brand_raw"]

def ping():
    if get_os == 'Windows':
        ping_res = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True, encoding="cp850")
    elif get_os == 'Linux':
        ping_res = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True)
    else:
        return "N/A"

    txt = ping_res.stdout

    for line in txt.splitlines():
        # Fr/En
        if "Moyenne =" in line or "Average =" in line:
            fig = line.split("=")[-1].replace("ms", "").strip()
            return fig

    return "Error"

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

# CPU Temperature
def get_cpu_temp():
    if get_os == 'Windows':
        return None
    elif get_os == 'Linux':
        data = psutil.sensors_temperatures()
        if not data:
            return None
        measures = next(iter(data.values()))
        return measures[0].current
    else:
        return "N/A"

# Processes fuction
def get_top_proc():
    grouped = {}

    psutil.cpu_percent(interval=None) 
    
    for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_full_info']):
        try:
            if proc.info['memory_full_info'] is None:
                continue
            cpu = proc.info['cpu_percent']
            name = proc.info['name']
            ramMB = proc.info['memory_full_info'].uss // 1024**2

            if name == "System Idle Process" or name is None:
                continue
                
            if name in grouped:
                grouped[name]['cpu'] += cpu
                grouped[name]['ram'] += ramMB
            else:
                grouped[name] = {'name': name, 'cpu': cpu, 'ram': ramMB}

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    for name in grouped:
        grouped[name]['cpu'] = round(grouped[name]['cpu'] / cores, 2)

    grp_proc = grouped.values()
    proc_list = list(grp_proc)

    top3_cpu = sorted(proc_list, key=lambda x: x['cpu'], reverse=True)[:3]
    top3_ram = sorted(proc_list, key=lambda x: x['ram'], reverse=True)[:3]
    return top3_cpu, top3_ram

# Main function
def status():
    global last_recv, last_sent
    os.system('cls' if os.name == 'nt' else 'clear')

    print(f"{Fore.BLUE}==={Fore.RESET}{Fore.YELLOW } Py{Fore.RESET}{Fore.CYAN}SysMonitor{Fore.RESET} {Fore.BLUE}V1.0.1 ==={Fore.RESET}")
    print('')

    print(f"Machine name: {platform.node()}")
    print(f"Os : {get_os} {get_os_ver}")
    # Uptime
    boot_time = psutil.boot_time()
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(boot_time)
    print(f"Uptime : {str(uptime).split('.')[0]}")
    
    print('')
    print(Fore.BLUE + "---CPU---" + Fore.RESET)

    # CPU
    print(f"CPU       : {cpu_name}")

    cpusage = psutil.cpu_percent()
    cpu_bar = make_bar(cpusage)
    print(f"CPU Usage : {cpu_bar} {color_use(cpusage)}")

    cpu_freq = psutil.cpu_freq().current / 1000
    print(f"CPU Freq  : {cpu_freq:.1f} GHz")

    temp = get_cpu_temp()
    if temp is not None:
        print(f"CPU Temp  : {color_temp(temp)}")
    elif get_os == 'Windows':
        print(f"CPU Temp  : {Fore.YELLOW}N/A (Windows){Fore.RESET}")
    else:
        print("CPU Temp  : N/A")

    print('')
    print(Fore.BLUE + "---RAM---" + Fore.RESET)
    # Memory 
    ram = psutil.virtual_memory()
    ram_bar = make_bar(ram.percent)
    print(f"RAM Usage : {ram_bar} {color_use(ram.percent)} {ram.used // 1024**2} MB / {ram.total // 1024**2} MB")
    
    swram = psutil.swap_memory()
    print(f"SWAP RAM  : {color_use(swram.percent)} ({swram.used // 1024**2} MB / {swram.total // 1024**2} MB)")

    print('')
    print(Fore.BLUE + "---GPU---" + Fore.RESET)

    # GPU
    gpus = GPUtil.getGPUs()
    if not gpus:
        print(Fore.RED + "GPU: No GPU detected")
    else:
        for gpu in gpus:
            print(f"GPU       : {gpu.name}")
            gpu_use = gpu.load*100
            gpu_bar = make_bar(gpu_use)
            print(f"GPU Usage : {gpu_bar} {color_use(gpu_use)}")
            print(f"GPU Temp  : {color_temp(gpu.temperature)}")
            # VRAM
            vram_percent = round((gpu.memoryUsed / gpu.memoryTotal) * 100, 1)
            vram_bar = make_bar(vram_percent)
            print(f"VRAM Usage: {vram_bar} {color_use(vram_percent)} {gpu.memoryUsed:.0f} MB / {gpu.memoryTotal:.0f} MB")

    print('')
    print(Fore.BLUE + "---DISKS---" + Fore.RESET)

    # Disk
    seen = set()
    IGNORED_FS = {"tmpfs", "devtmpfs", "squashfs", "overlay"}

    for p in psutil.disk_partitions():
        if p.device in seen:
            continue
        seen.add(p.device)

        if p.fstype in IGNORED_FS:
            continue

        try:
            usage = psutil.disk_usage(p.mountpoint)

            free_text = f"{usage.free / (1024**3):.2f} GB"
            used_text = f"{usage.used / (1024**3):.2f} GB"
            
            colored_free = color_disk(free_text, usage.percent)
            colored_used = color_disk(used_text, usage.percent)
            
            print(f"Disk {p.mountpoint} Free {colored_free} | Used {colored_used}")

        except PermissionError:
            continue

    print('')
    print(Fore.BLUE + "---NETWORK---" + Fore.RESET)

    # Network
    actual = psutil.net_io_counters()
    spd_dwnld = actual.bytes_recv - last_recv
    spd_upld = actual.bytes_sent - last_sent
    last_recv = actual.bytes_recv
    last_sent = actual.bytes_sent
    print(f"Download speed : {spd_dwnld / (1024):.2f} kB/s")
    print(f"Upload speed   : {spd_upld / (1024):.2f} kB/s")
    ping_net = ping()
    print(f"Ping           : {ping_net} ms")



    print("")
    print(Fore.BLUE + "---TOP PROCESSES---" + Fore.RESET)
    
    # Inside status()
    cpu_list, ram_list = get_top_proc()

    print(f"{'--- TOP CPU ---':<30} | {'--- TOP RAM ---':<30}")

    # Iterate through both lists using zip
    for c, r in zip(cpu_list, ram_list):
        cpu_proc = c['name'][:15].ljust(15)
        cpu_val = color_use(c['cpu'])
        left_col = f"{cpu_proc} : {cpu_val}"

        ram_name = r['name'][:15].ljust(15)
        ram_val = f"{r['ram']} Mo"
        right_col = f"{ram_name} : {ram_val}"

        print(f"{left_col:<40} | {right_col}")
        
   # print("=====================")

try:
    while True:
        status()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")