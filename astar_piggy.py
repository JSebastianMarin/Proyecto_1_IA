import heapq

def a_star(self, start, goal):

    """Realiza la búsqueda A* desde start hasta goal."""
    def heuristic(a, b):
        """Calcula la distancia Manhattan entre dos puntos a y b."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    start = tuple(start)
    goal = tuple(goal)
    
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    if start == tuple(self.cookie_pos):
        self.eaten_cookie = True 

    if self.eaten_cookie:
        self.step_price = 0.5
    print(self.step_price)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return self.reconstruct_path(came_from, current)

        # Coordenadas de movimiento (arriba, abajo, izquierda, derecha)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in moves:
            neighbor = (current[0] + dx, current[1] + dy)
            neighbor = tuple(neighbor)
            
            if 0 <= neighbor[0] < 4 and 0 <= neighbor[1] < 5 and list(neighbor) not in self.wall_positions:
                tentative_g_score = g_score[current] + self.step_price

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # Si no se encuentra un camino

def reconstruct_path(self, came_from, current):
    """Reconstruye el camino desde el diccionario came_from."""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path