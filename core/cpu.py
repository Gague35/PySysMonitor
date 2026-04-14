import psutil
import platform
import cpuinfo

get_os = platform.system()
get_os_ver = (f'{platform.release()} | Version: {platform.version()}')
machine_name = platform.node()
cores = psutil.cpu_count()
cpu_name = cpuinfo.get_cpu_info()["brand_raw"]

def format_uptime(uptime):
    days = uptime.days
    hours = uptime.seconds // 3600
    minutes = (uptime.seconds % 3600) // 60
    seconds = uptime.seconds % 60
    if days > 0:
        return f"{days}d {hours}h {minutes}m {seconds}s"
    else:
        return f"{hours}h {minutes}m {seconds}s"

def get_cpu_temp():
    if get_os == 'Windows':
        return None
    elif get_os == 'Linux':
        data = psutil.sensors_temperatures()
        if not data:
            return None
        measures = next(iter(data.values()))
        return round(measures[0].current, 1)
    else:
        return "N/A"
    
def get_cpu_usage():
    return psutil.cpu_percent()

def get_cpu_freq():
    return round(psutil.cpu_freq().current / 1000, 2)