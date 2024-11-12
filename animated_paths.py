import random

def animate_piggy_path(self):
    """Anima el movimiento de Piggy hacia Kermit recalculando el camino en cada paso."""
    def move_step():

        if self.power <= 12:
            # Buscar el nuevo camino hacia Kermit con A*
            path = self.a_star(self.piggy_pos, self.current_kermit_pos)
            piggy_img = self.piggy_rage
            if not path:
                return  # Si no hay camino, detener la animación
        else:
            # Buscar el nuevo camino hacia Kermit con BFS
            path = self.bfs_move_piggy(self.piggy_pos, self.current_kermit_pos)
            self.power = random.randint(1, 10)
            piggy_img = self.piggy
            if not path:
                return  # Si no hay camino, detener la animación

        # Si Piggy está en la posición inicial, no mover en el primer paso
        if self.piggy_pos == [2, 3]:
            next_pos = path[0]  # Mantener la posición inicial
        else:
            next_pos = path[1]  # Mover Piggy una casilla en el camino

        self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].config(image=self.camino_piggy)
        self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].image = self.camino_piggy

        self.piggy_pos = next_pos
        self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].config(image=piggy_img)
        self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].image = piggy_img

        if self.current_kermit_pos == self.elmo_pos:
            return

        if tuple(self.current_kermit_pos) == self.piggy_pos:
            self.found = True
            self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].config(image=self.piggy_found_kermit)
            self.grid_labels[self.piggy_pos[0]][self.piggy_pos[1]].image = self.piggy_found_kermit
            self.show_alert("¡Piggy ha encontrado a Kermit!")
            return


        # Llamar a la siguiente animación después de un breve retraso
        self.root.after(1000, move_step)

    # Iniciar la animación
    move_step()

def animate_kermit_path(self, path):

    """Anima el movimiento de Kermit a lo largo del camino encontrado."""
    def move_step(step):
        
        if self.found:
            return

        if step >= len(path):
            return

        # Borrar la imagen de Kermit de la celda anterior
        if step > 0:
            prev_pos = path[step - 1]
            
            if prev_pos == self.cookie_pos:
                self.grid_labels[prev_pos[0]][prev_pos[1]].config(image=self.cookie)
                self.grid_labels[prev_pos[0]][prev_pos[1]].image = self.cookie
            else:
                # Cambiar la imagen de la celda anterior a la imagen de camino de Kermit
                self.grid_labels[prev_pos[0]][prev_pos[1]].config(image=self.camino_kermit)
                self.grid_labels[prev_pos[0]][prev_pos[1]].image = self.camino_kermit

        # Colocar la imagen de Kermit en la nueva celda
        current_pos = path[step]
        self.current_kermit_pos = current_pos
        self.grid_labels[current_pos[0]][current_pos[1]].config(image=self.kermit)
        self.grid_labels[current_pos[0]][current_pos[1]].image = self.kermit

        # Actualizar la posición de Kermit después de cada paso
        self.kermit_pos = current_pos

        if self.current_kermit_pos == self.elmo_pos:
            self.grid_labels[current_pos[0]][current_pos[1]].config(image=self.kermit_found_elmo)
            self.grid_labels[current_pos[0]][current_pos[1]].image = self.kermit_found_elmo
            self.show_alert("¡Kermit ha encontrado a Elmo!")
            return
        
        if tuple(self.current_kermit_pos) == self.piggy_pos:
            self.grid_labels[current_pos[0]][current_pos[1]].config(image=self.piggy_found_kermit)
            self.grid_labels[current_pos[0]][current_pos[1]].image = self.piggy_found_kermit
            self.found = True
            self.show_alert("¡Piggy ha encontrado a Kermit!")
            return   

        # Llamar a la siguiente animación después de un breve retraso
        self.root.after(1000, move_step, step + 1)

    # Iniciar la animación desde el primer paso
    move_step(0)