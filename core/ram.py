import psutil

def get_ram():
    return psutil.virtual_memory()

def get_swap():
    return psutil.swap_memory()