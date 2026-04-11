import psutil
import GPUtil
import os
import subprocess
import platform
import time
import datetime
from colorama import Fore
from core.cpu import get_cpu_temp, get_cpu_usage, get_cpu_freq, cpu_name, get_os, get_os_ver, cores
from core.ram import get_ram, get_swap
from core.gpu import get_gpus
from core.disks import get_disks
from core.network import get_network_speed, get_ping
from core.processes import get_top_proc

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

    cpusage = get_cpu_usage()
    cpu_bar = make_bar(cpusage)
    print(f"CPU Usage : {cpu_bar} {color_use(cpusage)}")

    print(f"CPU Freq  : {get_cpu_freq():.1f} GHz")

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
    ram = get_ram()
    ram_bar = make_bar(ram.percent)
    print(f"RAM Usage : {ram_bar} {color_use(ram.percent)} {ram.used // 1024**2} MB / {ram.total // 1024**2} MB")
    
    swram = get_swap()
    print(f"SWAP RAM  : {color_use(swram.percent)} ({swram.used // 1024**2} MB / {swram.total // 1024**2} MB)")

    print('')
    print(Fore.BLUE + "---GPU---" + Fore.RESET)

    # GPU
    gpus = get_gpus()
    if not gpus:
        print(Fore.RED + "GPU: No GPU detected")
    else:
        for gpu in gpus:
            print(f"GPU       : {gpu.name}")
            gpu_use = round(gpu.load*100, 1)
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
    for disks in get_disks():
        colored_free = color_disk(disks['free'], disks['percent'])
        colored_used = color_disk(disks['used'], disks['percent'])
        print(f"Disk {disks['mountpoint']} Free {colored_free} GB | Used {colored_used} GB")


    print('')
    print(Fore.BLUE + "---NETWORK---" + Fore.RESET)

    # Network
    net = get_network_speed()
    print(f"Download: {net['download']} MB/s")
    print(f"Upload: {net['upload']} MB/s")

    ping = get_ping()
    print(f"Ping : {ping} ms")

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
        
try:
    while True:
        status()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")