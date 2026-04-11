import customtkinter as ctk

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
ctk.CTkLabel(cpu_frame, text="Usage : 45%", anchor="center", font=FONT).grid(row=1, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(cpu_frame, text="Fréq : 3.2 GHz", anchor="center", font=FONT).grid(row=3, column=0, pady=10, padx=20, sticky="ew")
ctk.CTkLabel(cpu_frame, text="Temp : 65°C", anchor="center", font=FONT).grid(row=4, column=0, pady=2, padx=20, sticky="ew")

# RAM
ctk.CTkLabel(ram_frame, text="Usage : 60%", anchor="center", font=FONT).grid(row=1, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(ram_frame, text="21354 MB / 32549 MB", anchor="center", font=FONT).grid(row=2, column=0, pady=0, padx=20, sticky="ew")
ctk.CTkLabel(ram_frame, text="SWAP : 10%", anchor="center", font=FONT).grid(row=4, column=0, pady=5, padx=20, sticky="ew" )
ctk.CTkLabel(ram_frame, text="984 MB / 8192 MB", anchor="center", font=FONT).grid(row=5, column=0, pady=0, padx=20, sticky="ew" )

# GPU
ctk.CTkLabel(gpu_frame, text="Usage : 80%", anchor="center", font=FONT).grid(row=1, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(gpu_frame, text="Temp : 70°C", anchor="center", font=FONT).grid(row=3, column=0, pady=10, padx=20, sticky="ew")
ctk.CTkLabel(gpu_frame, text="VRAM : 50% | 4096 MB / 8192 MB", anchor="center", font=FONT).grid(row=4, column=0, pady=2, padx=20, sticky="ew")

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
ctk.CTkLabel(disk_frame, text="C:\ — Free: 120.50 GB | Used: 80.30 GB", anchor="center", font=FONT).grid(row=1, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(disk_frame, text="D:\ — Free: 500.00 GB | Used: 200.00 GB", anchor="center", font=FONT).grid(row=2, column=0, pady=2, padx=20, sticky="ew")

# Network
ctk.CTkLabel(net_frame, text="Download : 150.00 kB/s", anchor="center", font=FONT).grid(row=1, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(net_frame, text="Upload : 20.00 kB/s", anchor="center", font=FONT).grid(row=2, column=0, pady=2, padx=20, sticky="ew" )
ctk.CTkLabel(net_frame, text="Ping : 12 ms", anchor="center", font=FONT).grid(row=3, column=0, pady=2, padx=20, sticky="ew")

# Frames ROW 3
processes_frame = ctk.CTkFrame(app, corner_radius=10)
processes_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

processes_frame.grid_columnconfigure(0, weight=1)
processes_frame.grid_columnconfigure(1, weight=1)


# Titles ROW 3
ctk.CTkLabel(processes_frame, text="--- TOP CPU ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=0, pady=5)
ctk.CTkLabel(processes_frame, text="--- TOP RAM ---", text_color="#4DA6FF", font=FONT_TITLE).grid(row=0, column=1, pady=5)

# TOP CPU
ctk.CTkLabel(processes_frame, text="opera: 9.7%", anchor="center", font=FONT).grid(row=2, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(processes_frame, text="code: 7.4%", anchor="center", font=FONT).grid(row=3, column=0, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(processes_frame, text="spotify: 5.5%", anchor="center", font=FONT).grid(row=4, column=0, pady=2, padx=20, sticky="ew")


# TOP RAM
ctk.CTkLabel(processes_frame, text="opera: 9.7%", anchor="center", font=FONT).grid(row=2, column=1, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(processes_frame, text="code: 7.4%", anchor="center", font=FONT).grid(row=3, column=1, pady=2, padx=20, sticky="ew")
ctk.CTkLabel(processes_frame, text="spotify: 5.5%", anchor="center", font=FONT).grid(row=4, column=1, pady=2, padx=20, sticky="ew")

app.mainloop()