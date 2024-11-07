import tkinter as tk
from PIL import Image, ImageTk

def create_grid(self, rows, cols):
    # Crear un frame para la cuadrícula centrado
    grid_frame = tk.Frame(self.root, bg='black')  # Fondo negro para el frame
    grid_frame.pack(pady=10, padx=10, expand=True)

    # Crear celdas en la cuadrícula
    for r in range(rows):
        row_labels = []
        for c in range(cols):
            # Crear una celda con imagen por defecto
            cell = tk.Label(grid_frame, bg='black', borderwidth=1, relief='solid')  # Fondo negro para las celdas
            cell.grid(row=r, column=c, padx=2, pady=2)
            
            # Asignar imagen por defecto a todas las celdas
            cell.config(image=self.void)
            cell.image = self.void  # Guardar referencia a la imagen
            
            row_labels.append(cell)  # Almacenar las etiquetas en una lista
        self.grid_labels.append(row_labels)  # Almacenar las filas

def load_images(self):
    # Cargar y redimensionar imágenes usando Pillow
    self.void = self.resize_image("Imagenes/default.png")  # Imagen por defecto
    self.elmo = self.resize_image("Imagenes/elmo.png")
    self.cookie = self.resize_image("Imagenes/galleta.png")
    self.kermit = self.resize_image("Imagenes/kermit.png")
    self.piggy = self.resize_image("Imagenes/piggy.png")
    self.wall = self.resize_image("Imagenes/muro.png")  # Cargar la imagen del muro
    self.camino_kermit = self.resize_image("Imagenes/camino_kermit.png")  # Cargar la imagen del camino de Kermit
    self.camino_piggy = self.resize_image("Imagenes/camino_piggy.png")  # Cargar la imagen del camino de Piggy

def resize_image(self, image_path):
    # Redimensionar la imagen manteniendo la relación de aspecto
    img = Image.open(image_path)
    img = img.resize((self.cell_size, self.cell_size), Image.LANCZOS)  # Usar LANCZOS para calidad
    return ImageTk.PhotoImage(img)

def add_images(self):
    # Insertar imágenes en la matriz
    self.grid_labels[self.elmo_pos[0]][self.elmo_pos[1]].config(image=self.elmo)  # Coloca a Elmo en su posición
    for wall_pos in self.wall_positions:  # Colocar todos los muros
        self.grid_labels[wall_pos[0]][wall_pos[1]].config(image=self.wall)
    self.grid_labels[0][0].config(image=self.cookie)  # Coloca 'cookie' en la celda (0, 0)

    # Colocar a Kermit en su posición inicial
    self.grid_labels[self.kermit_pos[0]][self.kermit_pos[1]].config(image=self.kermit)
    self.grid_labels[self.kermit_pos[0]][self.kermit_pos[1]].image = self.kermit

    # Colocar a Piggy en su posición inicial
    self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].config(image=self.piggy)
    self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].image = self.piggy
