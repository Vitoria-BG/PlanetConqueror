from tkinter import *
import random

# Variables (constant)
GAME_WIDTH = 800
GAME_HEIGHT = 800
ITEM_SIZE = 50
BODY_LENGTH = 3
SPACESHIP_COLOR = "#b1b1b1"
PLANET_COLOR = "#0b8adf"
BACKGROUND_COLOR = "#000000"

# ----------------------------------------------------------------------------
class Spaceship:
    def __init__(self):
        self.body_size = BODY_LENGTH
        self.coordinates = []          # store coordinates
        self.squares = []              # store rectangles (canvas)

        for i in range(0, BODY_LENGTH):
            # start in the top-left
            self.coordinates.append([0,0])

        # draw each segment on the canvas
        for x_pos,y_pos in self.coordinates:
            square = canvas.create_rectangle(x_pos,                    # top-left X
                                             y_pos,                    # top-left Y
                                             x_pos + ITEM_SIZE,        # bottom-right X
                                             y_pos + ITEM_SIZE,        # bottom-right Y
                                             fill = SPACESHIP_COLOR,   # fill color
                                             tag = "rocket")           # object tag 
            # keep track of the rectangle
            self.squares.append(square) 

# ----------------------------------------------------------------------------
class Planet:
    def __init__(self):
        # random grid positions (pixels)
        x_pos = random.randint(0, (GAME_WIDTH//ITEM_SIZE)-1) * ITEM_SIZE
        y_pos = random.randint(0, (GAME_HEIGHT//ITEM_SIZE)-1) * ITEM_SIZE

        # store the planet's coordinates
        self.coordinates = [x_pos,y_pos]

        # draw the planet as an oval
        canvas.create_oval(x_pos, y_pos, x_pos+ITEM_SIZE, y_pos+ITEM_SIZE, fill=PLANET_COLOR, tag = "planet")     

# ----------------------------------------------------------------------------
def turn(spaceship, planet):   
    # current head coordinates of the spaceship
    x_pos,y_pos = spaceship.coordinates[0]

    # update coordinates based on new direction
    if direction == "up":
        y_pos -= ITEM_SIZE
    elif direction == "down":
        y_pos += ITEM_SIZE
    elif direction == "right":
        x_pos += ITEM_SIZE
    elif direction == "left":
        x_pos -= ITEM_SIZE

    # new coordinate of the head position 
    spaceship.coordinates.insert(0,(x_pos,y_pos))  # insert(index, element)

    # draw the new head as a rectangle
    square = canvas.create_rectangle(x_pos,y_pos, x_pos+ITEM_SIZE, y_pos+ITEM_SIZE, fill=SPACESHIP_COLOR)

    # new rectangle (head) position 
    spaceship.squares.insert(0,square)

    # if head coordinates = planet coordinates -> score
    if x_pos == planet.coordinates[0] and y_pos == planet.coordinates[1]:
        global score 
        global speed
        score += 1

        # update score on canvas
        label.config(text="{} planets conquered!".format(score))
        canvas.delete("planet")
        # new planet 
        planet = Planet()

        # for every 4 points 
        if score != 0 and score & 3 == 0:
            # decrease speed but never lower than 20
            speed = max(20, speed - 4)

    else:
        # remove last part of the spaceship to simulate movement
        del spaceship.coordinates[-1]
        canvas.delete(spaceship.squares[-1])
        del spaceship.squares[-1]

    # end the game on collision
    if collisions(spaceship):
        gameOver()

    else:
        # next turn -> delay SPEED
        window.after(speed, turn, spaceship, planet)

# ----------------------------------------------------------------------------
def changeDirection(nextDirection):
    global direction

    if nextDirection == "up":
        # prevent reversing
        if direction != "down":
            direction = nextDirection

    elif nextDirection == "down":
        # prevent reversing
        if direction != "up":
            direction = nextDirection

    elif nextDirection == "right":
        # prevent reversing
        if direction != "left":
            direction = nextDirection

    elif nextDirection == "left":
        # prevent reversing
        if direction != "right":
            direction = nextDirection

# ----------------------------------------------------------------------------
def collisions(spaceship):
    x_pos,y_pos = spaceship.coordinates[0]

    # check collision with walls
    if x_pos < 0 or x_pos >= GAME_WIDTH:
        return True
    elif y_pos < 0 or y_pos >= GAME_HEIGHT:
        return True

    # check collision with body
    for bodyPart in spaceship.coordinates[1:]:
        if x_pos == bodyPart[0] and y_pos == bodyPart[1]:
            return True
        
    # no collision
    return False

# ----------------------------------------------------------------------------
def gameOver():
    global restart_button

    # clear the canvas
    canvas.delete(ALL)

    # canvas center
    center_x = canvas.winfo_width() / 2
    center_y = (canvas.winfo_height() / 2 - 55)

     # draw text 
    canvas.create_text(center_x, center_y, font=("consolas", 70, "bold"), text="GAME OVER", fill="white")

    # restart button 
    restart_button = Button(window, text="Restart", font=("consolas", 20),bg="#0b8adf",activebackground="#0b6cc7", command=restartGame)
    restart_button.place(x = center_x - 60, y = center_y + 120)

# ----------------------------------------------------------------------------
def restartGame():
    global spaceship, planet, score, speed, direction, restart_button

    # reset game stats
    score = 0
    speed = 90
    label.config(text="{} planets conquered!".format(score))
    direction = "down"

    # clear canvas
    canvas.delete(ALL)

    # remove restart button
    try:
        restart_button.destroy()
    except:
        pass

    # recreate spaceship and planet
    spaceship = Spaceship()
    planet = Planet()

    # restart game loop
    turn(spaceship, planet)
    
# ----------------------------------------------------------------------------
window = Tk()

# CONTROLS 
window.bind('<Up>', lambda event: changeDirection("up"))
window.bind('<Down>', lambda event: changeDirection("down"))
window.bind('<Right>', lambda event: changeDirection("right"))
window.bind('<Left>', lambda event: changeDirection("left"))

# WINDOW DESIGN SETTINGS
window.title("Planet Conqueror")
window.resizable(False, False)

# initial conditions
score = 0 
speed = 90
direction = "down"

# label on window 
label = Label(window, text="{} planets conquered!".format(score), font=("consolas",30))
label.pack()

# canvas on window 
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# update UI -> process pending events
window.update()

# CENTERING THE WINDOW
# current window dimensions in pixels
window_width = window.winfo_width()
window_height = window.winfo_height()

# monitor width and height in pixels
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# X and Y coordinates -> where the window should start
start_x = int((screen_width/2) - (window_width/2))
start_y = int((screen_height/2) - (window_height/2))

# <width>x<height>+<pos_x>+<pos_y>
window.geometry(f"{window_width}x{window_height}+{start_x}+{start_y}")

# TO BEGIN THE GAME -> creating a class instance + call function
spaceship = Spaceship() 
planet = Planet() 
turn(spaceship,planet)

window.mainloop()
