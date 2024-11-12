import tkinter as tk

from gui_elements import create_grid, load_images, resize_image, add_images
from dls_kermit import dls_move_kermit, dls, try_move
from bfs_piggy import bfs_move_piggy, reconstruct_path_bfs
from astar_piggy import a_star, reconstruct_path
from animated_paths import animate_piggy_path, animate_kermit_path
from utils import show_alert
class GameEnvironmentGUI:
    def __init__(self, root):
        # Inicializar la ventana de la interfaz gráfica
        self.root = root
        self.root.title("Pacman Univalle")
        self.root.geometry("1200x900")
        self.root.configure(bg='White')  # Cambiar el fondo de la ventana a negro

        # Crear la matriz 4x5 y almacenar las etiquetas
        self.grid_labels = []
        self.cell_size = 200  # Tamaño de la celda

        # Cargar y redimensionar imágenes usando Pillow
        self.load_images()

        # Crear la cuadrícula después de cargar las imágenes
        self.create_grid(4, 5)

        # Crear varibale global para definir cuando kermit es encontrado por piggy
        self.found = False

        self.power = 5

        self.eaten_cookie = False
        
        # Coordenadas de movimiento (izquierda, abajo, arriba, derecha)
        self.moves = [(0, -1), (-1, 0), (1, 0), (0, 1)]

        # Posición inicial de Kermit, Elmo y Piggy
        self.kermit_pos = [0, 3]  # Posición inicial de Kermit
        self.elmo_pos = [2, 0]     # Posición de Elmo
        self.wall_positions = [[3, 1], [2, 1], [2, 2], [1,2]]  # Posiciones de varios muros
        self.piggy_pos = [2, 3]    # Posición inicial de Piggy
        self.cookie_pos = [1, 1]


        self.current_kermit_pos = self.kermit_pos

        # Insertar imágenes
        self.add_images()

        # Iniciar búsqueda DLS para mover a Kermit
        self.depth_limit = 7  # Límite de profundidad
        self.dls_move_kermit()

        # Iniciar la búsqueda para mover a Piggy
        self.step_price = 1 # Precio de un paso
        self.animate_piggy_path()

    def show_alert(self, message):
        show_alert(message, self.root)

#GUI Elements
GameEnvironmentGUI.create_grid = create_grid
GameEnvironmentGUI.load_images = load_images
GameEnvironmentGUI.resize_image = resize_image
GameEnvironmentGUI.add_images = add_images

#Depth Limited Search KERMIT
GameEnvironmentGUI.dls_move_kermit = dls_move_kermit
GameEnvironmentGUI.dls = dls
GameEnvironmentGUI.try_move = try_move

#Breadth First Search PIGGY
GameEnvironmentGUI.bfs_move_piggy = bfs_move_piggy
GameEnvironmentGUI.reconstruct_path_bfs = reconstruct_path_bfs

# A* Search PIGGY
GameEnvironmentGUI.a_star = a_star
GameEnvironmentGUI.reconstruct_path = reconstruct_path

#Animated Paths
GameEnvironmentGUI.animate_piggy_path = animate_piggy_path
GameEnvironmentGUI.animate_kermit_path = animate_kermit_path


def main():
    root = tk.Tk()
    game = GameEnvironmentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
