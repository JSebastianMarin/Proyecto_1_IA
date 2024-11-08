import tkinter as tk

from gui_elements import create_grid, load_images, resize_image, add_images
from dls_kermit import dls_move_kermit, dls, try_move
from bfs_piggy import check_piggy_movement, stop_piggy_animation, bfs_move_piggy, reconstruct_path
from aestrella_piggy import a_star, reconstruct_path
from animated_paths import astar_animate_piggy_path, animate_kermit_path

class GameEnvironmentGUI:
    def __init__(self, root):
        # Inicializar la ventana de la interfaz gráfica
        self.root = root
        self.root.title("Pacman Univalle")
        self.root.geometry("800x600")
        self.root.configure(bg='White')  # Cambiar el fondo de la ventana a negro

        # Crear la matriz 4x5 y almacenar las etiquetas
        self.grid_labels = []
        self.cell_size = 100  # Tamaño de la celda

        # Cargar y redimensionar imágenes usando Pillow
        self.load_images()

        # Crear la cuadrícula después de cargar las imágenes
        self.create_grid(4, 5)

        # Posición inicial de Kermit, Elmo y Piggy
        self.kermit_pos = [3, 2]  # Posición inicial de Kermit
        self.elmo_pos = [2, 0]     # Posición de Elmo
        self.wall_positions = [[3, 1], [2, 1], [0, 2], [0, 3]]  # Posiciones de varios muros
        self.piggy_pos = [0, 4]    # Posición inicial de Piggy

        self.current_kermit_pos = self.kermit_pos
        self.current_piggy_pos = self.piggy_pos
        # Variables para controlar la animación de Piggy
        #self.piggy_animating = False
        #self.piggy_animation_step = 0

        # Insertar imágenes
        self.add_images()

        # Iniciar búsqueda limitada por profundidad para mover a Kermit
        self.depth_limit = 7  # Límite de profundidad
        self.dls_move_kermit()

        # Iniciar la verificación constante de la posición de Kermit para Piggy
        #self.check_piggy_movement()

        # Iniciar la búsqueda A* para mover a Piggy hacia Kermit
        self.animate_piggy_path()


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
GameEnvironmentGUI.check_piggy_movement = check_piggy_movement
GameEnvironmentGUI.stop_piggy_animation = stop_piggy_animation
GameEnvironmentGUI.bfs_move_piggy = bfs_move_piggy
GameEnvironmentGUI.reconstruct_path = reconstruct_path

# A* Search PIGGY
GameEnvironmentGUI.a_star = a_star
GameEnvironmentGUI.reconstruct_path = reconstruct_path

#Animated Paths
GameEnvironmentGUI.animate_piggy_path = astar_animate_piggy_path
GameEnvironmentGUI.animate_kermit_path = animate_kermit_path


def main():
    root = tk.Tk()
    game = GameEnvironmentGUI(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()
