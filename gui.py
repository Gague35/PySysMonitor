import customtkinter as ctk
from core.cpu import get_cpu_usage, get_cpu_freq, get_cpu_temp, get_os
from core.ram import get_ram, get_swap
from core.gpu import get_gpus
from core.disks import get_disks
from core.network import get_network_speed, get_ping
from core.processes import get_top_proc

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("PySysMonitor")
app.geometry("1080x720")
app.resizable(False, False)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_rowconfigure(2, weight=1)
app.grid_rowconfigure(3, weight=1)

FONT = ("Consolas", 15)
FONT_TITLE = ("Trebuchet MS", 20, "bold")
FONT_HEADER = ("Segoe UI", 30, "bold")

# Title
title_frame = ctk.CTkFrame(app, fg_color="transparent", height=50)
title_frame.grid(row=0, column=0, columnspan=3, pady=7.5, sticky="ew")
title_frame.grid_propagate(False)

inner = ctk.CTkFrame(title_frame, fg_color="transparent")
inner.place(relx=0.487, rely=0.4, anchor="center")

title = ctk.CTkLabel(inner, text="Py", font=FONT_HEADER, text_color="#FFD700")
title.pack(side="left")

title2 = ctk.CTkLabel(inner, text="SysMonitor", font=FONT_HEADER, text_color="#00FFFF")
title2.pack(side="left")

# Frames ROW 1
cpu_frame = ctk.CTkFrame(app, corner_radius=10)
cpu_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
cpu_bar = ctk.CTkProgressBar(cpu_frame, corner_radius=10, width=50, height=10, progress_color="#4DA6FF")
cpu_bar.grid(row=2, column=0, pady=2, padx=20, sticky="ew")
cpu_bar.set(0.45)

ram_frame = ctk.CTkFrame(app, corner_radius=10)
ram_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
ram_bar = ctk.CTkProgressBar(ram_frame, corner_radius=10, width=50, height=10, progress_color="#4DA6FF")
ram_bar.grid(row=3, column=0, pady=2, padx=20, sticky="ew")
ram_bar.set(0.60)


gpu_frame = ctk.CTkFrame(app, corner_radius=10)
gpu_frame.grid(row=1, column=2, padx=10, pady=10, sticky="nsew")
gpu_bar = ctk.CTkProgressBar(gpu_frame, corner_radius=10, width=50, height=10, progress_color="#4DA6FF")
gpu_bar.grid(row=2, column=0, pady=2, padx=20, sticky="ew")
gpu_bar.set(0.80)
vram_bar = ctk.CTkProgressBar(gpu_frame, corner_radius=10, width=50, height=10, progress_color="#4DA6FF")
vram_bar.grid(row=5, column=0, pady=2, padx=20, sticky="ew")
vram_bar.set(0.60)

cpu_frame.grid_columnconfigure(0, weight=1)
ram_frame.grid_columnconfigure(0, weight=1)
gpu_frame.grid_columnconfigure(0, weight=1)

# Titles ROW 1
ctk.CTkLabel(cpu_frame, text="--- CPU ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)
ctk.CTkLabel(ram_frame, text="--- RAM ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)
ctk.CTkLabel(gpu_frame, text="--- GPU ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)

# CPU
cpu_usage_lab = ctk.CTkLabel(cpu_frame, text="Usage : 45%", anchor="center", font=FONT)
cpu_usage_lab.grid(row=1, column=0, pady=2, padx=20, sticky="ew")
cpu_freq_lab = ctk.CTkLabel(cpu_frame, text="Freq : 3.2 GHz", anchor="center", font=FONT)
cpu_freq_lab.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
cpu_temp_lab = ctk.CTkLabel(cpu_frame, text="Temp : 65°C", anchor="center", font=FONT)
cpu_temp_lab.grid(row=4, column=0, pady=2, padx=20, sticky="ew")

# RAM
ram_usage_lab =ctk.CTkLabel(ram_frame, text="Usage : 60%", anchor="center", font=FONT)
ram_usage_lab.grid(row=1, column=0, pady=2, padx=20, sticky="ew")
ram_total_lab =ctk.CTkLabel(ram_frame, text="21354 MB / 32549 MB", anchor="center", font=FONT)
ram_total_lab.grid(row=2, column=0, pady=0, padx=20, sticky="ew")
swap_usage_lab = ctk.CTkLabel(ram_frame, text="SWAP : 10%", anchor="center", font=FONT)
swap_usage_lab.grid(row=4, column=0, pady=5, padx=20, sticky="ew")
swap_total_lab = ctk.CTkLabel(ram_frame, text="984 MB / 8192 MB", anchor="center", font=FONT)
swap_total_lab.grid(row=5, column=0, pady=0, padx=20, sticky="ew")

# GPU
gpu_usage_lab = ctk.CTkLabel(gpu_frame, text="Usage : 80%", anchor="center", font=FONT)
gpu_usage_lab.grid(row=1, column=0, pady=2, padx=20, sticky="ew")
gpu_temp_lab = ctk.CTkLabel(gpu_frame, text="Temp : 70°C", anchor="center", font=FONT)
gpu_temp_lab.grid(row=3, column=0, pady=10, padx=20, sticky="ew")
vram_lab = ctk.CTkLabel(gpu_frame, text="VRAM : 50% | 4096 MB / 8192 MB", anchor="center", font=FONT)
vram_lab.grid(row=4, column=0, pady=2, padx=20, sticky="ew")

# Frames ROW 2
disk_frame = ctk.CTkFrame(app, corner_radius=10)
disk_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

net_frame = ctk.CTkFrame(app, corner_radius=10)
net_frame.grid(row=2, column=2, padx=10, pady=10, sticky="nsew")

disk_frame.grid_columnconfigure(0, weight=1)
net_frame.grid_columnconfigure(0, weight=1)

# Titles ROW 2
ctk.CTkLabel(disk_frame, text="--- Disks ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)
ctk.CTkLabel(net_frame, text="--- Network ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)

# Disk
disk_labs = []

# Network
net_download_lab = ctk.CTkLabel(net_frame, text="Download : 150.00 kB/s", anchor="center", font=FONT)
net_download_lab.grid(row=1, column=0, pady=2, padx=20, sticky="ew")
net_upload_lab = ctk.CTkLabel(net_frame, text="Upload : 20.00 kB/s", anchor="center", font=FONT)
net_upload_lab.grid(row=2, column=0, pady=2, padx=20, sticky="ew")
net_ping_lab = ctk.CTkLabel(net_frame, text="Ping : 12 ms", anchor="center", font=FONT)
net_ping_lab.grid(row=3, column=0, pady=2, padx=20, sticky="ew")

# Frames ROW 3
processes_frame = ctk.CTkFrame(app, corner_radius=10)
processes_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

processes_frame.grid_columnconfigure(0, weight=1)
processes_frame.grid_columnconfigure(1, weight=1)

# Titles ROW 3
ctk.CTkLabel(processes_frame, text="--- TOP CPU ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)
ctk.CTkLabel(processes_frame, text="--- TOP RAM ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=1, pady=5)

# TOP CPU
cpu_proc_labs = []
for i in range(3):
    lab = ctk.CTkLabel(processes_frame, text="...", anchor="center", font=FONT)
    lab.grid(row=i+2, column=0, pady=2, padx=20, sticky="ew")
    cpu_proc_labs.append(lab)

# TOP RAM
ram_proc_labs = []
for i in range(3):
    lab = ctk.CTkLabel(processes_frame, text="...", anchor="center", font=FONT)
    lab.grid(row=i+2, column=1, pady=2, padx=20, sticky="ew")
    ram_proc_labs.append(lab)


def update():
    # CPU
    cpu_usage = get_cpu_usage()
    cpu_usage_lab.configure(text=f"Usage : {cpu_usage}%")
    cpu_bar.set(cpu_usage / 100)
    cpu_freq = get_cpu_freq()
    cpu_freq_lab.configure(text=f" Freq : {cpu_freq} GHz")
    cpu_temp = get_cpu_temp()
    if cpu_temp is not None:
        cpu_temp_lab.configure(text=f"Temp : {cpu_temp}°C")
    elif get_os == 'Windows':
        cpu_temp_lab.configure(text="Temp : N/A (Windows)")
    else:
        cpu_temp_lab.configure(text="Temp : N/A")
    
    # RAM
    ram_usage = get_ram()
    ram_usage_lab.configure(text=f"Usage : {ram_usage.percent}%")
    ram_total_lab.configure(text=f"{ram_usage.used / (1024**2):.0f} MB / {ram_usage.total / (1024**2):.0f} MB")
    ram_bar.set(ram_usage.percent / 100)
    # SWAP 
    swap_usage = get_swap()
    swap_usage_lab.configure(text=f"SWAP : {swap_usage.percent}%")
    swap_total_lab.configure(text=f"{swap_usage.used / (1024**2):.0f} MB / {swap_usage.total / (1024**2):.0f}")

    # GPU
    gpu_usage = get_gpus()
    if gpu_usage:
        gpu_usage = gpu_usage[0]
        gpu_usage_lab.configure(text=f"Usage : {round(gpu_usage.load*100, 1)}%")
        gpu_bar.set(gpu_usage.load)
        gpu_temp_lab.configure(text=f"Temp : {gpu_usage.temperature}°C")
        vram_percent = round((gpu_usage.memoryUsed / gpu_usage.memoryTotal) * 100, 1)
        vram_lab.configure(text=f"VRAM : {vram_percent}% | {gpu_usage.memoryUsed:.0f} MB / {gpu_usage.memoryTotal:.0f} MB")
        vram_bar.set(vram_percent / 100)

    # Disks
    for lab in disk_labs:
        lab.destroy()
    disk_labs.clear()

    for i, disk in enumerate(get_disks()):
        lab = ctk.CTkLabel(disk_frame, text=f"{disk['mountpoint']} — Free: {disk['free']} GB | Used: {disk['used']} GB", anchor="center", font=FONT)
        lab.grid(row=i+1, column=0, pady=2, padx=20, sticky="ew")
        disk_labs.append(lab)

    # Network
    net_speed = get_network_speed()
    net_download_lab.configure(text=f"Download : {net_speed['download']} kB/s")
    net_upload_lab.configure(text=f"Upload : {net_speed['upload']} kB/s")
    net_ping = get_ping()
    net_ping_lab.configure(text=f"Ping : {net_ping} ms")

    # Processes
    cpu_list, ram_list = get_top_proc()
    for i, proc in enumerate(cpu_list):
        cpu_proc_labs[i].configure(text=f"{proc['name']} : {proc['cpu']}%")
    for r, proc in enumerate(ram_list):
        ram_proc_labs[r].configure(text=f"{proc['name']} : {proc['ram']} MB")

    app.after(1000, update)

update()

app.mainloop()