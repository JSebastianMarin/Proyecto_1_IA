import tkinter as tk
from PIL import Image, ImageTk
from collections import deque

from dls_kermit import dls_move_kermit, dls, try_move
from gui_elements import create_grid, load_images, resize_image, add_images
from animated_paths import animate_piggy_path, animate_kermit_path


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
        self.kermit_pos = [0, 4]  # Posición inicial de Kermit
        self.elmo_pos = [2, 0]     # Posición de Elmo
        self.wall_positions = [[3, 1], [2, 1], [1, 2], [2, 2]]  # Posiciones de varios muros
        self.piggy_pos = [2, 3]    # Posición inicial de Piggy

        # Variables para controlar la animación de Piggy
        self.piggy_animating = False
        self.piggy_animation_step = 0

        # Insertar imágenes
        self.add_images()

        # Iniciar búsqueda limitada por profundidad para mover a Kermit
        self.depth_limit = 7  # Límite de profundidad
        self.dls_move_kermit()

        # Iniciar la verificación constante de la posición de Kermit para Piggy
        self.check_piggy_movement()

    

    def check_piggy_movement(self):
        """Revisa constantemente la posición de Kermit y mueve a Piggy si es necesario."""
        if self.kermit_pos == self.piggy_pos:
            self.stop_piggy_animation()  # Detener la animación actual de Piggy
        self.bfs_move_piggy()
        self.root.after(1000, self.check_piggy_movement)  # Revisar cada segundo

    def stop_piggy_animation(self):
        """Detiene la animación actual de Piggy."""
        self.piggy_animating = False

    def bfs_move_piggy(self):
        """Inicia la búsqueda por amplitud (BFS) para mover a Piggy hacia Kermit."""
        queue = deque([self.piggy_pos])  # Cola para BFS
        visited = set()  # Conjunto de posiciones visitadas
        parent = {tuple(self.piggy_pos): None}  # Para reconstruir el camino

        while queue:
            current_pos = queue.popleft()

            # Si encontramos a Kermit, reconstruimos el camino y animamos
            if current_pos == self.kermit_pos:
                path = self.reconstruct_path(parent, current_pos)
                self.animate_piggy_path(path)
                return

            # Marcar esta posición como visitada
            visited.add(tuple(current_pos))

            # Coordenadas de movimiento (arriba, abajo, izquierda, derecha)
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for move in moves:
                new_pos = [current_pos[0] + move[0], current_pos[1] + move[1]]

                # Comprobar si la nueva posición está dentro de los límites
                if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 5:
                    # Comprobar si la nueva posición no es un muro y no ha sido visitada
                    if new_pos not in self.wall_positions and tuple(new_pos) not in visited:
                        queue.append(new_pos)
                        parent[tuple(new_pos)] = current_pos

    def reconstruct_path(self, parent, end_pos):
        """Reconstruye el camino desde el final hasta el inicio usando el diccionario parent."""
        path = []
        current = end_pos
        while current is not None:
            path.append(current)
            current = parent.get(tuple(current))
        path.reverse()  # Invertir el camino para que vaya desde el inicio hasta el final
        return path

#GUI Elements
GameEnvironmentGUI.create_grid = create_grid
GameEnvironmentGUI.load_images = load_images
GameEnvironmentGUI.resize_image = resize_image
GameEnvironmentGUI.add_images = add_images

#Depth Limited Search KERMIT
GameEnvironmentGUI.dls_move_kermit = dls_move_kermit
GameEnvironmentGUI.dls = dls
GameEnvironmentGUI.try_move = try_move

#Animated Paths
GameEnvironmentGUI.animate_piggy_path = animate_piggy_path
GameEnvironmentGUI.animate_kermit_path = animate_kermit_path

def main():
    root = tk.Tk()
    game = GameEnvironmentGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
