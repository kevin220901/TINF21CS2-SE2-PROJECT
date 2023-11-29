hor = 30
vert = 30
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = f'{hor},{vert}'
import pgzrun
from pgzero.actor import *
import pygame as pg
from settings import *


WIDTH = 1000
HEIGHT = 700

start = 20
end = 40

blokus_1piece = Actor("blokus_1piece")
blokus_2piece = Actor("blokus_2piece")

def draw_grid(self):
    for x in range(0, WIDTH, TILESIZE):
        pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, TILESIZE):
        pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))


def draw():
    screen.fill((0, 0, 0))
    offset_x = 50 # Verschiebung, damit das Grid nicht oben in der Ecke beginnt
    offset_y = 50
    feld = 20
    draw_grid()
    pg.display.flip()


#blokus_1piece.draw()
#blokus_2piece.draw()

def place_piece():
    blokus_1piece.x = 50
    blokus_1piece.y = 50

    blokus_2piece.x = 155
    blokus_2piece.y = 155

place_piece()

pgzrun.go()