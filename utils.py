import tkinter as tk
from tkinter import messagebox

def show_alert(message, rootGUI):
    root = tk.Tk()    # Crear la ventana principal
    root.withdraw()         # Ocultar la ventana principal
    messagebox.showinfo("Encontrado", message)  # Mostrar el cuadro de diálogo
    root.destroy()
    rootGUI.destroy()  # Cerrar la ventana principal