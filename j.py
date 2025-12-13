import tkinter as tk
import random

# Configuración del juego
WIDTH = 600
HEIGHT = 400
CELL = 20

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake con Tkinter")

        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="black")
        self.canvas.pack()

        self.reset()
        self.root.bind("<KeyPress>", self.change_direction)
        self.game_loop()

    def reset(self):
        self.direction = "Right"
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.random_food()
        self.score = 0
        self.game_over = False

    def random_food(self):
        return (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))

    def change_direction(self, event):
        key = event.keysym
        dirs = {"Up": "Up", "Down": "Down", "Left": "Left", "Right": "Right"}

        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        if key in dirs and self.direction != opposites[key]:
            self.direction = key

    def move_snake(self):
        x, y = self.snake[0]

        if self.direction == "Up":
            y -= CELL
        elif self.direction == "Down":
            y += CELL
        elif self.direction == "Left":
            x -= CELL
        elif self.direction == "Right":
            x += CELL

        new_head = (x, y)

        # Colisión con paredes
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            self.game_over = True
            return

        # Colisión consigo misma
        if new_head in self.snake:
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        # Colisión con comida
        if new_head == self.food:
            self.food = self.random_food()
            self.score += 1
        else:
            self.snake.pop()

    def draw(self):
        self.canvas.delete("all")

        # Dibujar comida
        fx, fy = self.food
        self.canvas.create_rectangle(fx, fy, fx + CELL, fy + CELL, fill="red")

        # Dibujar serpent
        for x, y in self.snake:
            self.canvas.create_rectangle(x, y, x + CELL, y + CELL, fill="green")

        # Dibujar marcador
        self.canvas.create_text(
            50, 10, fill="white", text=f"Score: {self.score}", font=("Arial", 14)
        )

        if self.game_over:
            self.canvas.create_text(
                WIDTH // 2, HEIGHT // 2,
                fill="white",
                font=("Arial", 24),
                text="GAME OVER\nPresiona R para reiniciar"
            )
            self.root.bind("<KeyPress-r>", self.restart)

    def restart(self, event):
        self.reset()

    def game_loop(self):
        if not self.game_over:
            self.move_snake()

        self.draw()
        self.root.after(100, self.game_loop)

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
