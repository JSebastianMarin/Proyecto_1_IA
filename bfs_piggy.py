from collections import deque

def check_piggy_movement(self, start_pos, end_pos):
    """Revisa constantemente la posición de Kermit y mueve a Piggy si es necesario."""
    if start_pos == end_pos:
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
        if current_pos == self.current_kermit_pos:
            path = self.reconstruct_path_bfs(parent, current_pos)
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

def reconstruct_path_bfs(self, parent, end_pos):
    """Reconstruye el camino desde el final hasta el inicio usando el diccionario parent."""
    path = []
    current = end_pos
    while current is not None:
        path.append(current)
        current = parent.get(tuple(current))
    path.reverse()  # Invertir el camino para que vaya desde el inicio hasta el final
    return path
