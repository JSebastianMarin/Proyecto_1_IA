import tkinter as tk
import random
from collections import deque
from queue import PriorityQueue

# Definimos la clase del entorno del juego con la interfaz gráfica
class GameEnvironmentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de René y Piggy")
        
        # Tamaño del tablero
        self.rows = 6
        self.cols = 9
        
        # Creación de la cuadrícula (usamos botones)
        self.buttons = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid = [
            ['.', '.', '.', '.', 'G', '.', '.', '.', 'E'],
            ['.', '#', '#', '#', '.', '#', '.', '#', '.'],
            ['.', '.', '.', '#', '.', '.', '#', '.', '.'],
            ['.', '#', '.', '#', '.', '.', '.', '.', '.'],
            ['R', '.', '.', '.', '#', '#', '#', '.', 'P'],
            ['#', '#', '.', '.', '.', '.', '#', '#', '#']
        ]
        
        # Iniciar posiciones de los personajes
        self.rené_pos = (0, 0)  # Inicialmente René está en la posición (0, 0)
        self.elmo_pos = (0, 8)   # Elmo está en la posición (0, 8)
        self.piggy_pos = (4, 8)  # Piggy está en la posición (4, 8)

        # Crear los botones que representan las casillas del tablero
        self.create_grid()

        # Variables de estado
        self.game_over = False

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                button = tk.Button(self.root, text='', width=6, height=3, 
                                   command=lambda x=i, y=j: self.cell_clicked(x, y))
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[i][j] = button
                self.update_button(i, j)
    
    def update_button(self, i, j):
        """Actualiza el texto y color de cada celda según el contenido"""
        cell = self.grid[i][j]
        if cell == 'R':
            self.buttons[i][j].config(bg='green', text='Rene')
        elif cell == 'E':
            self.buttons[i][j].config(bg='red', text='Elmo')
        elif cell == 'P':
            self.buttons[i][j].config(bg='purple', text='Piggy')
        elif cell == 'G':
            self.buttons[i][j].config(bg='yellow', text='Galleta')
        elif cell == '#':
            self.buttons[i][j].config(bg='gray', text='Obstáculo')
        else:
            self.buttons[i][j].config(bg='white', text='')
    
    def move_agent(self, agent, new_pos):
        """Mueve al agente en el tablero"""
        x, y = new_pos
        if 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != '#':
            # Limpiar la posición anterior del agente
            if agent == 'R':
                self.grid[self.rené_pos[0]][self.rené_pos[1]] = '.'
                self.rené_pos = new_pos
            elif agent == 'P':
                self.grid[self.piggy_pos[0]][self.piggy_pos[1]] = '.'
                self.piggy_pos = new_pos

            # Colocar al agente en la nueva posición
            if agent == 'R':
                self.grid[self.rené_pos[0]][self.rené_pos[1]] = 'R'
            elif agent == 'P':
                self.grid[self.piggy_pos[0]][self.piggy_pos[1]] = 'P'

            # Actualizar la interfaz
            self.update_button(self.rené_pos[0], self.rené_pos[1])
            self.update_button(self.piggy_pos[0], self.piggy_pos[1])

    def check_win(self):
        if self.rené_pos == self.elmo_pos:
            print("¡René ha encontrado a Elmo!")
            self.game_over = True
        elif self.piggy_pos == self.rené_pos:
            print("¡Piggy ha encontrado a René!")
            self.game_over = True

    def start_game(self):
        """Inicia el juego: mueve a René y a Piggy por turnos"""
        if self.game_over:
            return

        # Mueve a René utilizando la Búsqueda Limitada por Profundidad
        print("René está buscando a Elmo...")
        result_rene = self.depth_limited_search(self.rené_pos, max_depth=10)
        if result_rene:
            self.move_agent('R', result_rene)
        else:
            print("René no encontró a Elmo.")
        
        # Verifica si el juego terminó
        self.check_win()
        if self.game_over:
            return
        
        # Mueve a Piggy
        print("Ahora es el turno de Piggy...")
        if random.random() < 0.4:
            print("Piggy usa A* para encontrar a René.")
            self.a_star_search(self.piggy_pos)
        else:
            print("Piggy usa BFS para encontrar a René.")
            self.breadth_first_search(self.piggy_pos)
        
        # Verifica si el juego terminó
        self.check_win()

    # Algoritmo de Búsqueda Limitada por Profundidad
    def depth_limited_search(self, start, max_depth=10):
        def dfs(node, depth):
            if depth > max_depth:
                return None
            if node == self.elmo_pos:
                return node
            
            moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            x, y = node
            for dx, dy in moves:
                new_pos = (x + dx, y + dy)
                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and self.grid[new_pos[0]][new_pos[1]] != '#':
                    result = dfs(new_pos, depth + 1)
                    if result:
                        return result
            return None
        
        return dfs(start, 0)

    # Algoritmo de Búsqueda por Amplitud (BFS)
    def breadth_first_search(self, start):
        queue = deque([start])
        visited = set()
        visited.add(start)
        
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            current_pos = queue.popleft()
            if current_pos == self.rené_pos:
                print("¡Piggy ha encontrado a René!")
                self.move_agent('P', current_pos)
                return True
            
            x, y = current_pos
            for dx, dy in moves:
                new_pos = (x + dx, y + dy)
                if 0 <= new_pos[0] < self.rows and 0 <= new_pos[1] < self.cols and self.grid[new_pos[0]][new_pos[1]] != '#':
                    if new_pos not in visited:
                        visited.add(new_pos)
                        queue.append(new_pos)
        return False

    # Algoritmo A* para Piggy
    def a_star_search(self, start):
        goal = self.rené_pos
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        
        open_list = PriorityQueue()
        open_list.put((0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: heuristic(start, goal)}
        
        while not open_list.empty():
            current_f, current = open_list.get()
            if current == goal:
                self.move_agent('P', current)
                print("¡Piggy ha encontrado a René usando A*!")
                return True
            
            x, y = current
            for dx, dy in moves:
                neighbor = (x + dx, y + dy)
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols and self.grid[neighbor[0]][neighbor[1]] != '#':
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                        open_list.put((f_score[neighbor], neighbor))
        return False

# Función para iniciar la interfaz gráfica
def main():
    root = tk.Tk()
    game = GameEnvironmentGUI(root)
    
    start_button = tk.Button(root, text="Iniciar Juego", width=20, command=game.start_game)
    start_button.grid(row=game.rows, column=0, columnspan=game.cols, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
