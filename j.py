import tkinter as tk
import random

# ================= CONFIGURACIÓN =================
WIDTH = 600
HEIGHT = 400
CELL = 20

ROWS = 10
COLS = 10

GRID_WIDTH = COLS * CELL
GRID_HEIGHT = ROWS * CELL

OFFSET_X = (WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2

GAME_SPEED = 200
WIN_SCORE = 87
# =================================================


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake con Tkinter")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.state = "menu"
        self.apple_count = 1

        self.canvas.bind("<Button-1>", self.handle_click)
        self.root.bind("<KeyPress>", self.change_direction)

        self.reset()
        self.game_loop()

    # ----------------- RESET -----------------
    def reset(self):
        self.direction = "Right"
        self.next_direction = self.direction
        self.snake = [(5, 5), (4, 5), (3, 5)]
        self.food = [self.random_food() for _ in range(self.apple_count)]
        self.score = 0
        self.game_over = False

    # ----------------- COMIDA -----------------
    def random_food(self):
        while True:
            pos = (
                random.randint(0, COLS - 1),
                random.randint(0, ROWS - 1)
            )

            if pos in self.snake:
                continue

            if hasattr(self, "food") and pos in self.food:
                continue

            return pos

    # ----------------- CONTROLES -----------------
    def change_direction(self, event):
        if self.state != "game":
            return

        opposites = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

        if event.keysym in opposites:
            if self.direction != opposites[event.keysym]:
                self.next_direction = event.keysym

        if event.keysym.lower() == "r" and self.game_over:
            self.reset()

    # ----------------- MOVIMIENTO -----------------
    def move_snake(self):
        self.direction = self.next_direction

        col, row = self.snake[0]

        if self.direction == "Up":
            row -= 1
        elif self.direction == "Down":
            row += 1
        elif self.direction == "Left":
            col -= 1
        elif self.direction == "Right":
            col += 1

        new_head = (col, row)

        if col < 0 or col >= COLS or row < 0 or row >= ROWS:
            self.game_over = True
            return

        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head in self.food:
            self.food.remove(new_head)
            self.food.append(self.random_food())
            self.score += 1

            if self.score >= WIN_SCORE:
                self.state = "win"
                return
        else:
            self.snake.pop()

    # ----------------- DIBUJO -----------------
    def draw_grid(self):
        for r in range(ROWS):
            for c in range(COLS):
                x1 = OFFSET_X + c * CELL
                y1 = OFFSET_Y + r * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="darkgreen",
                    fill="#074607"
                )

    def draw_head(self, col, row):
        x = OFFSET_X + col * CELL
        y = OFFSET_Y + row * CELL

        if self.direction == "Up":
            points = [x + CELL/2, y, x, y + CELL, x + CELL, y + CELL]
        elif self.direction == "Down":
            points = [x, y, x + CELL, y, x + CELL/2, y + CELL]
        elif self.direction == "Left":
            points = [x, y + CELL/2, x + CELL, y, x + CELL, y + CELL]
        else:
            points = [x, y, x + CELL, y + CELL/2, x, y + CELL]

        self.canvas.create_polygon(points, fill="blue")

    def draw_game(self):
        self.canvas.delete("all")
        self.draw_grid()

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

        head_col, head_row = self.snake[0]
        self.draw_head(head_col, head_row)

        for col, row in self.snake[1:]:
            self.canvas.create_rectangle(
                OFFSET_X + col * CELL,
                OFFSET_Y + row * CELL,
                OFFSET_X + col * CELL + CELL,
                OFFSET_Y + row * CELL + CELL,
                fill="blue"
            )

        self.canvas.create_text(
            60, 20,
            fill="white",
            text=f"Score: {self.score}",
            font=("Arial", 14)
        )

        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                fill="white",
                font=("Arial", 24),
                text="GAME OVER\nPulsa R para reiniciar"
            )

    # ----------------- MENÚ -----------------
    def draw_menu(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            WIDTH // 2, 70,
            text="SNAKE",
            fill="white",
            font=("Arial", 36, "bold")
        )

        self.canvas.create_text(
            WIDTH // 2, 130,
            text="Número de manzanas",
            fill="white",
            font=("Arial", 16)
        )

        for i, value in enumerate([1, 3, 5]):
            x = WIDTH // 2 - 100 + i * 100
            color = "green" if self.apple_count == value else "gray"

            self.canvas.create_rectangle(
                x - 30, 160, x + 30, 200,
                fill=color
            )
            self.canvas.create_text(x, 180, text=str(value), fill="white")

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

    # ----------------- VICTORIA -----------------
    def draw_win(self):
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

    # ----------------- CLICS -----------------
    def handle_click(self, event):
        if self.state == "menu":
            for i, value in enumerate([1, 3, 5]):
                x = WIDTH // 2 - 100 + i * 100
                if x - 30 <= event.x <= x + 30 and 160 <= event.y <= 200:
                    self.apple_count = value

            if WIDTH // 2 - 80 <= event.x <= WIDTH // 2 + 80 and 240 <= event.y <= 290:
                self.state = "game"
                self.reset()

        elif self.state == "win":
            if WIDTH // 2 - 120 <= event.x <= WIDTH // 2 + 120 and 240 <= event.y <= 290:
                self.state = "menu"

    # ----------------- LOOP -----------------
    def game_loop(self):
        if self.state == "menu":
            self.draw_menu()
        elif self.state == "game":
            if not self.game_over:
                self.move_snake()
            self.draw_game()
        elif self.state == "win":
            self.draw_win()

        self.root.after(GAME_SPEED, self.game_loop)


# ================= EJECUCIÓN =================
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
