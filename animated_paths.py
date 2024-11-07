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
        self.grid_labels[current_pos[0]][current_pos[1]].config(image=self.kermit)
        self.grid_labels[current_pos[0]][current_pos[1]].image = self.kermit

        # Llamar a la siguiente animación después de un breve retraso
        self.root.after(500, move_step, step + 1)

    # Iniciar la animación desde el primer paso
    move_step(0)