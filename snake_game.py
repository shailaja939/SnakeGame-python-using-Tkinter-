# Snake Game with Resume and Pause Feature
from tkinter import *
import random

# ---------------- GAME SETTINGS ---------------- #
GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 20
SPEED = 100
BODY_PARTS = 3

SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

score = 0
direction = "down"
paused = False
game_running = True

# ---------------- PLAYER DETAILS ---------------- #
player_name = input("Enter Player Name: ")
player_id = input("Enter Player ID: ")

# ---------------- SNAKE CLASS ---------------- #
class Snake:

    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake"
            )

            self.squares.append(square)

# ---------------- FOOD CLASS ---------------- #
class Food:

    def __init__(self):

        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x,
            y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food"
        )

# ---------------- MAIN GAME FUNCTION ---------------- #
def next_turn(snake, food):

    global score

    if paused or not game_running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x,
        y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    # Food collision
    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1

        label.config(text=f"Score: {score}")

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # Collision checking
    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)

# ---------------- CHANGE DIRECTION ---------------- #
def change_direction(new_direction):

    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction

    elif new_direction == 'right' and direction != 'left':
        direction = new_direction

    elif new_direction == 'up' and direction != 'down':
        direction = new_direction

    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

# ---------------- CHECK COLLISIONS ---------------- #
def check_collisions(snake):

    x, y = snake.coordinates[0]

    # Wall collision
    if x < 0 or x >= GAME_WIDTH:
        return True

    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Self collision
    for body_part in snake.coordinates[1:]:

        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# ---------------- PAUSE / RESUME ---------------- #
def toggle_pause(event=None):

    global paused

    paused = not paused

    if paused:
        pause_label.config(text="PAUSED")
    else:
        pause_label.config(text="")
        next_turn(snake, food)

# ---------------- RESTART GAME ---------------- #
def restart_game(event=None):

    global score, direction, paused, game_running
    global snake, food

    score = 0
    direction = "down"
    paused = False
    game_running = True

    label.config(text=f"Score: {score}")
    pause_label.config(text="")

    canvas.delete(ALL)

    snake = Snake()
    food = Food()

    next_turn(snake, food)

# ---------------- GAME OVER ---------------- #
def game_over():

    global game_running

    game_running = False

    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 100,
        font=('Arial', 30, 'bold'),
        text="GAME OVER",
        fill="red"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 - 40,
        font=('Arial', 20),
        text=f"Player Name: {player_name}",
        fill="white"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2,
        font=('Arial', 20),
        text=f"Player ID: {player_id}",
        fill="white"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 40,
        font=('Arial', 24, 'bold'),
        text=f"Final Score: {score}",
        fill="yellow"
    )

    canvas.create_text(
        GAME_WIDTH / 2,
        GAME_HEIGHT / 2 + 100,
        font=('Arial', 16),
        text="Press R to Restart",
        fill="cyan"
    )

# ---------------- CREATE WINDOW ---------------- #
window = Tk()

window.title("Snake Game")

window.resizable(False, False)

# Score Label
label = Label(
    window,
    text=f"Score: {score}",
    font=('Arial', 20)
)

label.pack()

# Pause Label
pause_label = Label(
    window,
    text="",
    font=('Arial', 18, 'bold'),
    fg="red"
)

pause_label.pack()

# Canvas
canvas = Canvas(
    window,
    bg=BACKGROUND_COLOR,
    height=GAME_HEIGHT,
    width=GAME_WIDTH
)

canvas.pack()

window.update()

# Center Window
window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Keyboard Controls
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Pause / Resume using Spacebar
window.bind('<space>', toggle_pause)

# Restart using R key
window.bind('<r>', restart_game)
window.bind('<R>', restart_game)

# Start Game
snake = Snake()
food = Food()

next_turn(snake, food)
window.mainloop()