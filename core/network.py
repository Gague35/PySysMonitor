import psutil
import subprocess
import threading
import time
from core.cpu import get_os

last_recv = psutil.net_io_counters().bytes_recv
last_sent = psutil.net_io_counters().bytes_sent
last_ping = "..."

def get_network_speed():
    global last_recv, last_sent

    actual = psutil.net_io_counters()
    spd_dwnld = actual.bytes_recv - last_recv
    spd_upld = actual.bytes_sent - last_sent
    last_recv = actual.bytes_recv
    last_sent = actual.bytes_sent
    return {
        'download': round(spd_dwnld / (1024), 2),
        'upload': round(spd_upld / (1024), 2)
            }

def ping_loop():
    global last_ping
    while True:
        if get_os == 'Windows':
            ping_res = subprocess.run(["ping", "-n", "1", "8.8.8.8"], capture_output=True, text=True, encoding="cp850")
        elif get_os == 'Linux':
            ping_res = subprocess.run(["ping", "-c", "1", "8.8.8.8"], capture_output=True, text=True)
        else:
            last_ping = "N/A"
            time.sleep(5)
            continue
        
        txt = ping_res.stdout
            
        for line in txt.splitlines():
            # Windows Fr/En
            if "Moyenne =" in line or "Average =" in line:
                fig = line.split("=")[-1].replace("ms", "").strip()
                last_ping = fig
            # Linux
            if "rtt" in line or "round-trip" in line:
                fig = round(float(line.split("/")[4].strip()), 1)
                last_ping = fig
        
        time.sleep(5)

def get_ping():
    return last_ping

ping_thread = threading.Thread(target=ping_loop, daemon=True)
ping_thread.start()
