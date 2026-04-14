import psutil
import platform
import cpuinfo

get_os = platform.system()
get_os_ver = (f'{platform.release()} | Version: {platform.version()}')
cores = psutil.cpu_count()
cpu_name = cpuinfo.get_cpu_info()["brand_raw"]

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