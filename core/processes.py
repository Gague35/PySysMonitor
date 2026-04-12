import psutil
from core.cpu import cores

def total_proc():
    return len(list(psutil.process_iter()))

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