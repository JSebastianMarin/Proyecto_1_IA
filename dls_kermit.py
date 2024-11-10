def dls_move_kermit(self):
    """Inicia la búsqueda limitada por profundidad (DLS) para mover a Kermit."""
    # Variables para la búsqueda
    visited = set()
    path = []

    # Ejecutar búsqueda limitada por profundidad (DLS)
    if self.dls(self.kermit_pos, visited, path, 0, self.depth_limit):
        # Si se encuentra un camino, mover a Kermit
        self.animate_kermit_path(path)
    else: self.show_alert("¡Kermit no ha encontrado un camino hacia Elmo!")


def dls(self, pos, visited, path, depth, limit):
    """Algoritmo DLS para buscar el camino hasta la posición de Elmo."""
    # Si alcanzamos el límite de profundidad, detener la pbúsqueda
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

    # Intentar movimientos en el nuevo orden
    for i in range(4):
        if i == 0:  # Intentar hacia arriba primero
            new_pos = [pos[0] + self.moves[0][0], pos[1] + self.moves[0][1]]
            if self.try_move(new_pos, visited, path, depth, limit):
                return True
        elif i == 1:  # Intentar hacia abajo
            new_pos = [pos[0] + self.moves[1][0], pos[1] + self.moves[1][1]]
            if self.try_move(new_pos, visited, path, depth, limit):
                return True
        elif i == 2:  # Intentar hacia la izquierda
            new_pos = [pos[0] + self.moves[2][0], pos[1] + self.moves[2][1]]
            if self.try_move(new_pos, visited, path, depth, limit):
                return True
        else:  # Intentar el siguiente movimiento en el orden normal
            new_pos = [pos[0] + self.moves[3][0], pos[1] + self.moves[3][1]]
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