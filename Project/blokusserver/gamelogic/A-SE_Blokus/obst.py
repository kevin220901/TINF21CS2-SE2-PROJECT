x = 0
y = 0
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'

from pgzero.actor import *
import pgzrun
from random import randint

WIDTH = 1280
HEIGHT = 720
score = 0

apple = Actor("apple")

def draw():
    screen.fill("green")
    apple.draw
    screen.draw.text("Punkte: " + str(score), color="black", topleft=(10,10))

def place_apple():
    apple.x = randint(10,800)
    apple.y = randint(10,600)

def on_mouse_down(pos):
    if apple.collidepoint(pos):
        print("Treffer")
        place_apple()
    else:
        print("Daneben")
        quit()

place_apple()

pgzrun.go()