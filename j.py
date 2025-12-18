import tkinter as tk
import random

# Configuración general del juego
# Dimensiones de la ventana principal
WIDTH = 600
HEIGHT = 400
CELL = 20  # Tamaño de cada casilla del grid en píxeles

# Tamaño del tablero en celdas
ROWS = 10
COLS = 10

# Cálculo del área jugable en píxeles
GRID_WIDTH = COLS * CELL
GRID_HEIGHT = ROWS * CELL

# Márgenes para centrar el tablero dentro de la ventana
OFFSET_X = (WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2

# Velocidad del juego  y puntuación para ganar
GAME_SPEED = 200
WIN_SCORE = 87


class SnakeGame:
    def __init__(self, root):
        # Referencia a la ventana principal
        self.root = root
        self.root.title("Snake con Tkinter")

        # Lienzo donde se dibuja todo el juego
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        # Estado inicial: menú principal
        self.state = "menu"
        # Número inicial de manzanas simultáneas
        self.apple_count = 1

        # Eventos de ratón y teclado
        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<KeyPress>", self.change_direction)

        # Iniciar el juego en estado limpio
        self.reset()
        # Arrancar el bucle principal del juego
        self.game_loop()

    def reset(self):
        # Reinicia la serpiente, la comida y la puntuación
        # Dirección por defecto hacia la derecha
        self.direction = "Right"
        self.next_direction = self.direction

        # La serpiente se representa como una lista de tuplas
        self.snake = [(5, 5), (4, 5), (3, 5)]

        # Generar tantas manzanas como se hayan configurado
        self.food = [self.random_food() for _ in range(self.apple_count)]

        # Reinicio de la puntuación y del estado de fin de partida
        self.score = 0
        self.game_over = False

    def random_food(self):
        # Devuelve una posición libre del tablero para colocar una manzana
        while True:
            pos = (
                random.randint(0, COLS - 1),
                random.randint(0, ROWS - 1)
            )

            # Evitar colocar comida encima de la serpiente
            if pos in self.snake:
                continue

            # Evitar solapar manzanas cuando hay varias
            if hasattr(self, "food") and pos in self.food:
                continue

            return pos

    def change_direction(self, event):
        # Gestiona las teclas de dirección y la tecla R para reiniciar
        # Si no estamos en partida, ignorar flechas
        if self.state != "game":
            return

        # Direcciones opuestas para evitar giro de 180 grados
        opposites = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

        # Cambio de dirección con las flechas
        if event.keysym in opposites:
            if self.direction != opposites[event.keysym]:
                # Se guarda la dirección que tomará en el siguiente movimiento
                self.next_direction = event.keysym

        # Tecla R para reiniciar cuando ya se ha perdido
        if event.keysym.lower() == "r" and self.game_over:
            self.reset()

    def move_snake(self):
        # Actualiza la posición de la serpiente un paso en la dirección actual
        # Aplicar la última dirección válida
        self.direction = self.next_direction

        # Cabeza de la serpiente
        col, row = self.snake[0]

        # Desplazar la cabeza según la dirección
        if self.direction == "Up":
            row -= 1
        elif self.direction == "Down":
            row += 1
        elif self.direction == "Left":
            col -= 1
        elif self.direction == "Right":
            col += 1

        new_head = (col, row)

        # Comprobar colisión con bordes del tablero
        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            self.game_over = True
            return

        # Comprobar choque contra sí misma
        if new_head in self.snake:
            self.game_over = True
            return

        # Insertar la nueva cabeza al principio de la lista
        self.snake.insert(0, new_head)

        # Si se ha comido una manzana, aumentar puntuación y reponer manzana
        if new_head in self.food:
            self.food.remove(new_head)
            self.food.append(self.random_food())
            self.score += 1

            # Condición de victoria cuando se alcanza cierta puntuación
            if self.score >= WIN_SCORE:
                self.state = "win"
                return
        else:
            # Si no come, la cola se acorta
            self.snake.pop()

    def draw_grid(self):
        # Dibuja el tablero de fondo con un grid
        for r in range(ROWS):
            for c in range(COLS):
                x1 = OFFSET_X + c * CELL
                y1 = OFFSET_Y + r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                # Cada celda es un rectángulo verde oscuro
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="darkgreen",
                    fill="#074607"
                )

    def draw_head(self, col, row):
        # Dibuja la cabeza de la serpiente con forma de triángulo
        x = OFFSET_X + col * CELL
        y = OFFSET_Y + row * CELL

        # Se ajustan los puntos del polígono según la dirección para “apuntar” hacia delante
        if self.direction == "Up":
            points = [x + CELL/2, y, x, y + CELL, x + CELL, y + CELL]
        elif self.direction == "Down":
            points = [x, y, x + CELL, y, x + CELL/2, y + CELL]
        elif self.direction == "Left":
            points = [x, y + CELL/2, x + CELL, y, x + CELL, y + CELL]
        else:
            # Right
            points = [x, y, x + CELL, y + CELL/2, x, y + CELL]

        self.canvas.create_polygon(points, fill="blue")

    def draw_game(self):
        # Redibuja todo el estado del juego 
        # Limpiar todo antes de volver a pintar
        self.canvas.delete("all")
        self.draw_grid()

        # Dibujar manzanas como círculos rojos
        for col, row in self.food:
            x1 = OFFSET_X + col * CELL
            y1 = OFFSET_Y + row * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            self.canvas.create_oval(
                x1, y1, x2, y2,
                fill="red",
                outline=""
            )

        # Primero se dibuja la cabeza
        head_col, head_row = self.snake[0]
        self.draw_head(head_col, head_row)

        # Y después el cuerpo como rectángulos
        for col, row in self.snake[1:]:
            self.canvas.create_rectangle(
                OFFSET_X + col * CELL,
                OFFSET_Y + row * CELL,
                OFFSET_X + col * CELL + CELL,
                OFFSET_Y + row * CELL + CELL,
                fill="blue"
            )

        # Marcador de puntuación arriba a la izquierda
        self.canvas.create_text(
            60, 20,
            fill="white",
            text=f"Puntuación: {self.score}",
            font=("Arial", 14)
        )

        # Mensaje de fin de juego
        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                fill="white",
                font=("Arial", 24),
                text="GAME OVER\nPulsa R para reiniciar"
            )

    def draw_menu(self):
        # Dibuja el menú principal con la selección de manzanas y el botón de iniciar
        self.canvas.delete("all")

        # Título principal
        self.canvas.create_text(
            WIDTH // 2, 70,
            text="SNAKE",
            fill="white",
            font=("Arial", 36, "bold")
        )

        # Texto explicando qué se está configurando
        self.canvas.create_text(
            WIDTH // 2, 130,
            text="Número de manzanas",
            fill="white",
            font=("Arial", 16)
        )

        # Botones de selección de cantidad de manzanas: 1, 3 o 5
        for i, value in enumerate([1, 3, 5]):
            x = WIDTH // 2 - 100 + i * 100
            color = "green" if self.apple_count == value else "gray"

            self.canvas.create_rectangle(
                x - 30, 160, x + 30, 200,
                fill=color
            )
            self.canvas.create_text(x, 180, text=str(value), fill="white")

        # Botón para iniciar la partida
        self.canvas.create_rectangle(
            WIDTH // 2 - 80, 240,
            WIDTH // 2 + 80, 290,
            fill="blue"
        )
        self.canvas.create_text(
            WIDTH // 2, 265,
            text="INICIAR",
            fill="white",
            font=("Arial", 16)
        )

    def draw_win(self):
        # Pantalla mostrada cuando se alcanza la puntuación objetivo
        self.canvas.delete("all")

        self.canvas.create_text(
            WIDTH // 2, 120,
            text="¡VICTORIA!",
            fill="gold",
            font=("Arial", 36, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2, 180,
            text=f"Puntuación final: {self.score}",
            fill="white",
            font=("Arial", 16)
        )

        # Botón para volver al menú principal
        self.canvas.create_rectangle(
            WIDTH // 2 - 120, 240,
            WIDTH // 2 + 120, 290,
            fill="green"
        )

        self.canvas.create_text(
            WIDTH // 2, 265,
            text="VOLVER AL MENÚ",
            fill="white",
            font=("Arial", 16)
        )

    def handle_click(self, event):
        # Procesa los clics del ratón según el estado del juego
        if self.state == "menu":
            # Comprobar si se ha hecho clic en alguna opción de número de manzanas
            for i, value in enumerate([1, 3, 5]):
                x = WIDTH // 2 - 100 + i * 100
                if x - 30 <= event.x <= x + 30 and 160 <= event.y <= 200:
                    self.apple_count = value

            # Comprobar si se ha pulsado el botón de INICIAR
            if WIDTH // 2 - 80 <= event.x <= WIDTH // 2 + 80 and 240 <= event.y <= 290:
                self.state = "game"
                self.reset()

        elif self.state == "win":
            # Volver al menú desde la pantalla de victoria
            if WIDTH // 2 - 120 <= event.x <= WIDTH // 2 + 120 and 240 <= event.y <= 290:
                self.state = "menu"

    def game_loop(self):
        # Bucle principal del juego, se ejecuta de forma periódica
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            # Sólo mover la serpiente si la partida sigue activa
            if not self.game_over:
                self.move_snake()
            self.draw_game()
        elif self.state == "win":
            self.draw_win()

        # Volver a llamar a game_loop tras un retardo
        self.root.after(GAME_SPEED, self.game_loop)


# Ejecución del programa principal
if __name__ == "__main__":
    # Crear la ventana principal de Tkinter y lanzar el juego
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()