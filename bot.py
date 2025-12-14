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

GAME_SPEED = 60
# =================================================


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Bot Perfecto")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.build_hamiltonian_cycle()
        self.reset()
        self.game_loop()

    # ----------------- HAMILTONIANO -----------------
    def build_hamiltonian_cycle(self):
        path = []

        for col in range(COLS):
            if col % 2 == 0:
                for row in range(ROWS):
                    path.append((col, row))
            else:
                for row in reversed(range(ROWS)):
                    path.append((col, row))

        self.next_cell = {}
        for i in range(len(path)):
            self.next_cell[path[i]] = path[(i + 1) % len(path)]

    # ----------------- RESET -----------------
    def reset(self):
        self.snake = [(0, 0), (0, 1), (0, 2)]
        self.score = 0
        self.game_over = False
        self.victory = False
        self.food = self.random_food()

    # ----------------- COMIDA -----------------
    def random_food(self):
        free_cells = [
            (c, r)
            for c in range(COLS)
            for r in range(ROWS)
            if (c, r) not in self.snake
        ]
        return random.choice(free_cells)

    # ----------------- BOT -----------------
    def move_snake(self):
        head = self.snake[0]
        new_head = self.next_cell[head]

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            if len(self.snake) == ROWS * COLS:
                self.victory = True
            else:
                self.food = self.random_food()
        else:
            self.snake.pop()

    # ----------------- DIBUJO -----------------
    def draw_grid(self):
        for row in range(ROWS):
            for col in range(COLS):
                x1 = OFFSET_X + col * CELL
                y1 = OFFSET_Y + row * CELL
                x2 = x1 + CELL
                y2 = y1 + CELL

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    outline="#0a5a0a",
                    fill="#0f7a0f"
                )

    def draw_head(self, col, row, next_col, next_row):
        x = OFFSET_X + col * CELL
        y = OFFSET_Y + row * CELL

        dx = next_col - col
        dy = next_row - row

        if dx == 1:
            points = [x, y, x + CELL, y + CELL / 2, x, y + CELL]
        elif dx == -1:
            points = [x + CELL, y, x, y + CELL / 2, x + CELL, y + CELL]
        elif dy == 1:
            points = [x, y, x + CELL, y, x + CELL / 2, y + CELL]
        else:
            points = [x + CELL / 2, y, x, y + CELL, x + CELL, y + CELL]

        self.canvas.create_polygon(points, fill="blue")

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid()

        # Comida
        fx, fy = self.food
        self.canvas.create_oval(
            OFFSET_X + fx * CELL + 4,
            OFFSET_Y + fy * CELL + 4,
            OFFSET_X + fx * CELL + CELL - 4,
            OFFSET_Y + fy * CELL + CELL - 4,
            fill="red",
            outline=""
        )

        # Cabeza
        head = self.snake[0]
        next_head = self.snake[1]
        self.draw_head(head[0], head[1], next_head[0], next_head[1])

        # Cuerpo
        for col, row in self.snake[1:]:
            self.canvas.create_rectangle(
                OFFSET_X + col * CELL,
                OFFSET_Y + row * CELL,
                OFFSET_X + col * CELL + CELL,
                OFFSET_Y + row * CELL + CELL,
                fill="blue"
            )

        # Score
        self.canvas.create_text(
            70, 20,
            fill="white",
            text=f"Score: {self.score}",
            font=("Arial", 14)
        )

        if self.victory:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                fill="gold",
                font=("Arial", 26, "bold"),
                text="¡VICTORIA!\nBOT PERFECTO"
            )

    # ----------------- LOOP -----------------
    def game_loop(self):
        if not self.victory:
            self.move_snake()

        self.draw()
        self.root.after(GAME_SPEED, self.game_loop)


# ================= EJECUCIÓN =================
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
