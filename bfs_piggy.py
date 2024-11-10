from collections import deque

def bfs_move_piggy(self, start, goal):
    
    start = tuple(start)
    goal = tuple(goal)

    """Inicia la búsqueda por amplitud (BFS) para mover a Piggy hacia Kermit."""
    queue = deque([start])  # Cola para BFS
    visited = set()  # Conjunto de posiciones visitadas
    parent = {start: None}  # Para reconstruir el camino

    while queue:
        current_pos = tuple(queue.popleft())

        # Si encontramos a Kermit, reconstruimos el camino y animamos
        if current_pos == goal:
            return self.reconstruct_path_bfs(parent, current_pos)

        # Marcar esta posición como visitada
        visited.add(tuple(current_pos))

        for move in self.moves:
            new_pos = [current_pos[0] + move[0], current_pos[1] + move[1]]

            # Comprobar si la nueva posición está dentro de los límites
            if 0 <= new_pos[0] < 4 and 0 <= new_pos[1] < 5:
                # Comprobar si la nueva posición no es un muro y no ha sido visitada
                if new_pos not in self.wall_positions and tuple(new_pos) not in visited:
                    queue.append(new_pos)
                    parent[tuple(new_pos)] = current_pos
    return self.show_alert("¡Piggy no ha encontrado un camino hacia Kermit!")

def reconstruct_path_bfs(self, parent, end_pos):
    """Reconstruye el camino desde el final hasta el inicio usando el diccionario parent."""
    path = []
    current = end_pos
    while current is not None:
        path.append(current)
        current = parent.get(tuple(current))
    path.reverse()  # Invertir el camino para que vaya desde el inicio hasta el final
    return path
