#Jonathan Dao
#Pac Man Project

import pygame as pg
from copy import copy
import game_functions as gf
from settings import Settings
from vector import Vector
from maze import Maze
from maze import GridPoint
from character import Pacman, Ghost
from math import atan2
from timer import Timer
from menu import MainMenu
from sound import Sound
import time


class Game:
    def __init__(self):
        pg.init()
        #window Settings
        pacImg = pg.image.load('images/PacR.png')
        #For Back Ground
        self.settings = Settings()
        self.screen = pg.display.set_mode(size=(self.settings.screen_width, self.settings.screen_height))
        self.display = pg.Surface((self.settings.screen_width, self.settings.screen_height))
        self.window = pg.display.set_mode(((self.settings.screen_width, self.settings.screen_height)))        
        pg.display.set_caption("PacMan Portal")
        pg.display.set_icon(pacImg)

        #Misc
        self.font = pg.font.SysFont(None, 48)
        self.maze = Maze(game = self)
        self.lives = 3
        self.score = 0
        self.PowerPhase = False
        self.PowerSwitched = False
        self.sound = Sound(bg_music="sounds/pacman_chomp.wav")
        #self.sound.play()
        self.occupied = 3

        nxt = self.maze.location(2, 4)
        grid_pt = self.maze.location(2, 5)
        prev = self.maze.location(2, 6)

        self.pacman = Pacman(game=self, v=Vector(-1, 0), grid_pt=grid_pt, grid_pt_next=nxt, grid_pt_prev=prev)
        self.pinky = Ghost(game=self, v=Vector(-1, 0), grid_pt=self.maze.location(6,5), grid_pt_next=self.maze.location(6,4), grid_pt_prev=self.maze.location(6,6), name="Pinky", number=0) 
        self.purpy = Ghost(game=self, v=Vector(-1, 0), grid_pt=self.maze.location(5,5), grid_pt_next=self.maze.location(5,4), grid_pt_prev=self.maze.location(5,6), name="Purpy", number=1) 
        self.greeny = Ghost(game=self, v=Vector(-1, 0), grid_pt=self.maze.location(5,6), grid_pt_next=self.maze.location(5,5), grid_pt_prev=self.maze.location(5,4), name="Greeny", number=2) 
        self.orangy = Ghost(game=self, v=Vector(-1, 0), grid_pt=self.maze.location(5,4), grid_pt_next=self.maze.location(5,6), grid_pt_prev=self.maze.location(5,5), name="Orangy", number=3) 
        self.orangy.Occupied = 3
        self.greeny.Occupied = 2
        self.purpy.Occupied = 1
        self.pinky.spawned = True 

        #Menu
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255) #not really black

        self.startMenu = MainMenu(self)
        self.UP_KEY, self.DOWN_KEY, self.PLAY_KEY, self.BACK_KEY = False, False, False, False
        self.grid = self.create_grid()
        self.finished = True
        self.restart()

    def to_grid(self, index):
        row = index // 11
        offset = index % 11
        ss = self.maze.location(row, offset)
        return ss

    def restart(self):
        self.startMenu.display_menu()

    def to_pixel(self, grid):
        pixels = []

    def create_grid(self):
        row0 = [0, 4, 6, 10]
        row1 = [x for x in range(11) if x != 5]
        row2 = copy(row1)
        row3 = [x for x in range(11) if x not in [1, 5, 9]]
        row4 = [2, 3, 5, 7, 8]
        row5 = [x for x in range(11) if x not in [4, 5, 6]]
        row6 = [x for x in range(3, 8, 1)]
        row7 = copy(row3)
        row8 = [x for x in range(11) if x not in [1, 5, 9]]
        row9 = copy(row3)
        rows = [row0, row1, row2, row3, row4, row5, row6, row7, row8, row8]

        i = 0
        for row in rows:
            print(f'row {i} = {row}');
            i += 1
        return rows

    def play(self):
        #self.sound.play()
        while not self.finished:
            self.startMenu.sound.pause_bg()
            if not self.sound.playing_bg:
                 self.sound.unpause_bg()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.startMenu.run_display = False
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pg.mouse.get_pos()
                    print('X: ' + mouseX + 'Y: ' + mouseY)
                elif event.type == pg.KEYDOWN: gf.check_keydown_events(event, self.pacman)
                elif event.type == pg.KEYUP: gf.check_keyup_events(event, self.pacman)

            # self.screen.fill(self.settings.bg_color)
            self.maze.update()
            self.pacman.update()
            self.pinky.update()
            self.purpy.update()
            self.greeny.update()
            self.orangy.update()

            #Check Eaten
            self.checkCollision(self.pinky)
            self.checkCollision(self.purpy)
            self.checkCollision(self.greeny)
            self.checkCollision(self.orangy)

            if self.pinky.spawned:
                self.pinky.move()
            if self.purpy.spawned:
                self.purpy.move()
            if self.greeny.spawned:
                self.greeny.move()
            if self.orangy.spawned:
                self.orangy.move()

            #Power Phase
            if self.PowerPhase == True:
                if not self.PowerSwitched:
                    sTime = time.time()
                    self.PowerSwitched = True
                    self.pinky.switchToRun()
                    self.purpy.switchToRun()
                    self.greeny.switchToRun()
                    self.orangy.switchToRun()
                eTime = time.time()
                dur = int(eTime - sTime)
                if dur >= 15:
                    self.PowerPhase = False
                    
            elif self.PowerPhase == False and self.PowerSwitched:
                self.pinky.switchToChase()
                self.purpy.switchToChase()
                self.greeny.switchToChase()
                self.orangy.switchToChase()
                self.PowerSwitched = False
            #pg.display.flip()
            pg.display.update()

    def checkCollision(self, character):
        char = character
        pacLoc = self.pacman.grid_pt
        charLoc = char.grid_pt

        if charLoc == pacLoc:
            if self.PowerPhase:
                char.die()
                self.pacman.KillGhost()
            else:
                self.pacman.die()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.PLAY_KEY, self.BACK_KEY = False, False, False, False

    def spawnGhost(self):
        if self.occupied > 0:
            if self.pinky.Occupied == self.occupied:
                self.pinky.spawnOut()
            elif self.purpy.Occupied == self.occupied:
                self.purpy.spawnOut()
            elif self.greeny.Occupied == self.occupied:
                self.greeny.spawnOut()
            elif self.orangy.Occupied == self.occupied:
                self.orangy.spawnOut()

    def check_events(self):
    # Watch for keyboard and mouse events.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.finished = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pg.mouse.get_pos()
            elif event.type == pg.KEYDOWN: gf.check_keydown_events(event=event, character=self.pacman)
            elif event.type == pg.KEYUP: gf.check_keyup_events(event=event, character=self.pacman)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.PLAY_KEY = True
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pg.K_UP:
                    self.UP_KEY = True

            if event.type == pg.KEYUP:
                if event.key == pg.K_RETURN:
                    self.PLAY_KEY = False
                if event.key == pg.K_BACKSPACE:
                    self.BACK_KEY = False
                if event.key == pg.K_DOWN:
                    self.DOWN_KEY = False
                if event.key == pg.K_UP:
                    self.UP_KEY = False     

def main():
    game = Game()
    game.play()


if __name__ == '__main__':

    main()

