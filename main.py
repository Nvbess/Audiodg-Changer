import ctypes
import psutil
import sys
import tkinter as tk
from tkinter import messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def funcion_principal():
    def find_process():
        for process in psutil.process_iter(['pid','name']):
            if process.info['name'] == 'audiodg.exe':
                return process
        return None

    audiodg = find_process()

    if audiodg:
        try:
            audiodg.nice(psutil.REALTIME_PRIORITY_CLASS)
            audiodg.cpu_affinity([0])
            messagebox.showinfo("Completado", "Prioridad y CPU cambiadas!")
        except psutil.AccessDenied:
            messagebox.showerror("Error", "Hubo un error al ejecutar el script :(")
    else:
        messagebox.showerror("Error", "audiodg.exe no se ha encontrado el proceso.")

if is_admin():
    app = tk.Tk()
    app.title("Cambiar audiodg.exe")

    frame = tk.Frame(app)
    frame.pack(padx=10, pady=10)

    button = tk.Button(frame, text="Cambiar CPU y Prioridad! :)", command=funcion_principal)
    button.pack(pady=5)

    app.mainloop()
else:
    # Re-ejecutar el script con permisos de administrador
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1)
