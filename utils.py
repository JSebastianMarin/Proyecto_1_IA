import tkinter as tk
from tkinter import messagebox

def show_alert(message, rootGUI):
    root = tk.Tk()    # Crear la ventana principal
    root.withdraw()         # Ocultar la ventana principal
    messagebox.showinfo("Alerta", message)  # Mostrar el cuadro de diálogo
    root.destroy()
    rootGUI.destroy()  # Cerrar la ventana principal

def viene_de(came_from, start, target):
    # Verificar si el target viene directamente del start
    if came_from.get(target) == start:
        return True
    # Verificar si el target tiene un predecesor y continuar la búsqueda
    elif target in came_from:
        return viene_de(came_from, start, came_from[target])
    else:
        return False