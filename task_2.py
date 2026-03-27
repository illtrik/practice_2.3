import tkinter as tk
import psutil

def update_stats():
    cpu_percent = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory()
    mem_used_percent = mem.percent
    mem_used_mb = mem.used / (1024 * 1024)
    mem_total_mb = mem.total / (1024 * 1024)
    disk = psutil.disk_usage('/')
    disk_percent = disk.percent

    cpu_label.config(text=f"Загрузка CPU: {cpu_percent}%")
    mem_label.config(text=f"Использование памяти: {mem_used_mb:.2f} MB / {mem_total_mb:.2f} MB ({mem_used_percent}%)")
    disk_label.config(text=f"Загрузка диска: {disk_percent}%")

    root.after(1000, update_stats)

root = tk.Tk()
root.title("Системный мониторинг")
root.geometry("400x150")

cpu_label = tk.Label(root, text="Загрузка CPU: ", font=("Arial", 14))
cpu_label.pack(pady=5)

mem_label = tk.Label(root, text="Использование памяти: ", font=("Arial", 14))
mem_label.pack(pady=5)

disk_label = tk.Label(root, text="Загрузка диска: ", font=("Arial", 14))
disk_label.pack(pady=5)

update_stats()

root.mainloop()