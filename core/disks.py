import psutil

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