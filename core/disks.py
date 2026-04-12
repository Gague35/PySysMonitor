import psutil

last_read = psutil.disk_io_counters().read_bytes
last_write = psutil.disk_io_counters().write_bytes

def get_disks():
    seen = set()
    IGNORED_FS = {"tmpfs", "devtmpfs", "squashfs", "overlay"}
    
    disks = []
    for p in psutil.disk_partitions():
        if p.device in seen:
            continue
        seen.add(p.device)

        if p.fstype in IGNORED_FS:
            continue

        try:
            usage = psutil.disk_usage(p.mountpoint)

            disks.append({
                'mountpoint': p.mountpoint,
                'free': round(usage.free / (1024**3), 2),
                'used': round(usage.used / (1024**3), 2),
                'percent': usage.percent
            })

        except PermissionError:
            continue
    return disks

def disk_speeds():
    global last_read, last_write
    dskspd = psutil.disk_io_counters()
    spd_read = dskspd.read_bytes - last_read
    spd_write = dskspd.write_bytes - last_write
    last_read = dskspd.read_bytes
    last_write = dskspd.write_bytes
    return spd_read, spd_write