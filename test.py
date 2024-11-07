
import tkinter as tk
from PIL import Image, ImageTk
from collections import deque

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
        self.current_pos_kermit = self.kermit_pos
        self.current_pos_piggy = self.piggy_pos

        # Variables para controlar la animación de Piggy
        self.piggy_animating = False
        self.piggy_animation_step = 0

        # Insertar imágenes
        self.add_images()

        # Iniciar búsqueda limitada por profundidad para mover a Kermit
        self.depth_limit = 6  # Límite de profundidad
        self.dls_move_kermit()

        # Iniciar la verificación constante de la posición de Kermit para Piggy
        self.check_piggy_movement()

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
        self.void = self.resize_image("default.png")  # Imagen por defecto
        self.elmo = self.resize_image("elmo.png")
        self.cookie = self.resize_image("galleta.png")
        self.kermit = self.resize_image("kermit.png")
        self.piggy = self.resize_image("piggy.png")
        self.wall = self.resize_image("muro.png")  # Cargar la imagen del muro
        self.camino_kermit = self.resize_image("camino_kermit.png")  # Cargar la imagen del camino de Kermit
        self.camino_piggy = self.resize_image("camino_piggy.png")  # Cargar la imagen del camino de Piggy

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
        self.grid_labels[1][1].config(image=self.cookie)  # Coloca 'cookie' en la celda (0, 0)

        # Colocar a Kermit en su posición inicial
        self.grid_labels[self.kermit_pos[0]][self.kermit_pos[1]].config(image=self.kermit)
        self.grid_labels[self.kermit_pos[0]][self.kermit_pos[1]].image = self.kermit

        # Colocar a Piggy en su posición inicial
        self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].config(image=self.piggy)
        self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].image = self.piggy

    def dls_move_kermit(self):
        """Inicia la búsqueda limitada por profundidad (DLS) para mover a Kermit."""
        # Variables para la búsqueda
        visited = set()
        path = []

        # Ejecutar búsqueda limitada por profundidad (DLS)
        if self.dls(self.kermit_pos, visited, path, 0, self.depth_limit):
            # Si se encuentra un camino, mover a Kermit
            self.animate_kermit_path(path)

    def dls(self, pos, visited, path, depth, limit):
        """Algoritmo DLS para buscar el camino hasta la posición de Elmo."""
        # Si alcanzamos el límite de profundidad, detener la búsqueda
        if depth > limit:
            return False

        # Si ya hemos visitado esta posición, la ignoramos
        if tuple(pos) in visited:
            return False

        # Marcar esta posición como visitada
        visited.add(tuple(pos))
        path.append(pos)

        # Si llegamos a la posición de Elmo, terminamos
        if pos == self.elmo_pos:
            return True

        # Orden de movimientos (arriba, abajo, izquierda, derecha)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Normal: arriba, abajo, izquierda, derecha

        # Intentar movimientos en el nuevo orden
        for i in range(4):
            if i == 0:  # Intentar hacia arriba primero
                new_pos = [pos[0] + moves[0][0], pos[1] + moves[0][1]]
                if self.try_move(new_pos, visited, path, depth, limit):
                    return True
            elif i == 1:  # Intentar hacia abajo
                new_pos = [pos[0] + moves[1][0], pos[1] + moves[1][1]]
                if self.try_move(new_pos, visited, path, depth, limit):
                    return True
            elif i == 2:  # Intentar hacia la izquierda
                new_pos = [pos[0] + moves[2][0], pos[1] + moves[2][1]]
                if self.try_move(new_pos, visited, path, depth, limit):
                    return True
            else:  # Intentar el siguiente movimiento en el orden normal
                new_pos = [pos[0] + moves[3][0], pos[1] + moves[3][1]]
                if self.try_move(new_pos, visited, path, depth, limit):
                    return True

        # Si no encontramos un camino, deshacemos el último movimiento
        visited.remove(tuple(pos))  # Permitir volver a explorar esta posición
        path.pop()
        return False

    def try_move(self, new_pos, visited, path, depth, limit):
        """Intenta un movimiento y verifica si hay un camino."""
        # Comprobar si la nueva posición está dentro de los límites
        if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 5:
            # Comprobar si la nueva posición no es un muro
            if new_pos not in self.wall_positions:  # Kermit no puede moverse a una celda con muro
                return self.dls(new_pos, visited, path, depth + 1, limit)
        return False

    def check_piggy_movement(self):
        """Revisa constantemente la posición de Kermit y mueve a Piggy si es necesario."""
        if self.kermit_pos == self.piggy_pos:
            self.stop_piggy_animation()  # Detener la animación actual de Piggy
        self.bfs_move_piggy()
        self.root.after(500, self.check_piggy_movement)  # Revisar cada medio segundo

    def stop_piggy_animation(self):
        """Detiene la animación actual de Piggy."""
        self.piggy_animating = False

    def bfs_move_piggy(self):
        """Inicia la búsqueda por amplitud (BFS) para mover a Piggy hacia Kermit."""
        queue = deque([self.piggy_pos])  # Cola para BFS
        visited = set()  # Conjunto de posiciones visitadas
        parent = {tuple(self.piggy_pos): None}  # Para reconstruir el camino

        while queue:
            current_pos_piggy = queue.popleft()

            # Si encontramos a Kermit, reconstruimos el camino y animamos
            if current_pos_piggy == self.current_pos_kermit:
                path = self.reconstruct_path(parent, current_pos_piggy)
                self.animate_piggy_path(path)
                return

            # Marcar esta posición como visitada
            visited.add(tuple(current_pos_piggy))

            # Coordenadas de movimiento (arriba, abajo, izquierda, derecha)
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for move in moves:
                new_pos = [current_pos_piggy[0] + move[0], current_pos_piggy[1] + move[1]]


                # Comprobar si la nueva posición está dentro de los límites
                if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 5:
                    # Comprobar si la nueva posición no es un muro y no ha sido visitada
                    if new_pos not in self.wall_positions and tuple(new_pos) not in visited:
                        queue.append(new_pos)
                        parent[tuple(new_pos)] = current_pos_piggy

        # Planificar la próxima búsqueda
        self.root.after(500, self.bfs_move_piggy)  # Repite la búsqueda cada 1000 ms (1 segundo)



    def reconstruct_path(self, parent, end_pos):
        """Reconstruye el camino desde el final hasta el inicio usando el diccionario parent."""
        path = []
        current = end_pos
        while current is not None:
            path.append(current)
            current = parent.get(tuple(current))
        path.reverse()  # Invertir el camino para que vaya desde el inicio hasta el final
        return path

    def animate_piggy_path(self, path):
        """Anima el movimiento de Piggy a lo largo del camino encontrado."""
        self.piggy_animating = True  # Marcar que Piggy está animando

        def move_step(step):
            if step >= len(path):
                return

            # Borrar la imagen de Piggy de la celda anterior
            if step > 0:
                prev_pos = path[step - 1]
                # Cambiar la imagen de la celda anterior a la imagen de camino de Piggy
                self.grid_labels[prev_pos[0]][prev_pos[1]].config(image=self.camino_piggy)
                self.grid_labels[prev_pos[0]][prev_pos[1]].image = self.camino_piggy

            # Colocar la imagen de Piggy en la nueva celda
            current_pos = path[step]
            self.current_pos_piggy = current_pos
            self.grid_labels[current_pos[0]][current_pos[1]].config(image=self.piggy)
            self.grid_labels[current_pos[0]][current_pos[1]].image = self.piggy

            # Llamar a la siguiente animación después de un breve retraso
            self.root.after(500, move_step, step + 1)

        # Iniciar la animación desde el primer paso
        move_step(0)

    def animate_kermit_path(self, path):
        """Anima el movimiento de Kermit a lo largo del camino encontrado."""
        def move_step(step):
            if step >= len(path):            
                return

            # Borrar la imagen de Kermit de la celda anterior
            if step > 0:
                prev_pos = path[step - 1]
                # Cambiar la imagen de la celda anterior a la imagen de camino de Kermit
                self.grid_labels[prev_pos[0]][prev_pos[1]].config(image=self.camino_kermit)
                self.grid_labels[prev_pos[0]][prev_pos[1]].image = self.camino_kermit

            # Colocar la imagen de Kermit en la nueva celda
            current_pos = path[step]
            self.current_pos_kermit = current_pos
            self.grid_labels[current_pos[0]][current_pos[1]].config(image=self.kermit)
            self.grid_labels[current_pos[0]][current_pos[1]].image = self.kermit

            # Llamar a la siguiente animación después de un breve retraso
            self.root.after(500, move_step, step + 1)

        # Iniciar la animación desde el primer paso
        move_step(0)

def main():
    root = tk.Tk()
    game = GameEnvironmentGUI(root)
    root.mainloop()

if __name__ == "__main__":  main()

