import sys
import pygame as pg
from vector import Vector
from math import fabs


swapped = False
li = [pg.K_RIGHT, pg.K_LEFT, pg.K_UP, pg.K_DOWN]
di = {pg.K_RIGHT : Vector(1, 0), pg.K_LEFT : Vector(-1, 0),
      pg.K_UP : Vector(0, -1), pg.K_DOWN : Vector(0, 1)}
epsilon = 0.0001

def compare(a, b): return fabs(a - b) < epsilon


def check_keydown_events(event, character):
    global swapped
    char = character

    if event.key in li and not swapped:
        v, new_dir = char.v, di[event.key]
        if not char.on_star():
            if compare(v.dot(new_dir), -1):
                char.reverse()
            return

        v = di[event.key]
        delta = (v.x if v.y == 0 else -11 * v.y)
        grid_pt = char.grid_pt
        idx = grid_pt.index
        possible_idx = idx + int(delta)
        if possible_idx in grid_pt.adj_list:
            char.grid_pt_prev.make_normal()
            char.grid_pt_next = char.to_grid(possible_idx)
            char.grid_pt_prev = grid_pt
            char.update_next_prev()

        char.v = di[event.key]
        char.scale_factor = 1.0
        char.update_angle()

    if event.key == pg.K_RIGHT: 
        character.dirR = True
    elif event.key == pg.K_LEFT: 
        character.dirL = True
    elif event.key == pg.K_UP: 
        character.dirU = True
    elif event.key == pg.K_DOWN: 
        character.dirD = True
    elif event.key == pg.K_q: 
        sys.exit()
    elif event.key == pg.K_SPACE:
        character.game.PowerPhase = True
        character.firePortalGun()
        #portal down

def check_keyup_events(event, character):
    global swapped
    if event.key in li and swapped:
        character.scale_factor = 0
        swapped = False

    if event.key == pg.K_RIGHT: character.dirR = False
    elif event.key == pg.K_LEFT: character.dirL = False
    elif event.key == pg.K_UP: character.dirU = False
    elif event.key == pg.K_DOWN: character.dirD = False