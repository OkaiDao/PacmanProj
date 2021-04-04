import pygame as pg
from pygame.sprite import Sprite
from timer import Timer
from sound import Sound

class Menu():
    
    pacR = [pg.image.load('images/PacR.png'), pg.image.load('images/PacRO.png')]
    pacRAnim = Timer(frames = pacR, wait = 300)
    bgImg = pg.image.load('images/maze.png')
    bgImg = pg.transform.rotozoom(bgImg, 0, 0.6)

    ghost1 = [pg.image.load('images/Ghost1_' + str(i + 1) + '.png') for i in range(2)]
    ghost2 = [pg.image.load('images/Ghost2_' + str(i + 1) + '.png') for i in range(2)]
    ghost3 = [pg.image.load('images/Ghost3_' + str(i + 1) + '.png') for i in range(2)]
    ghost4 = [pg.image.load('images/Ghost4_' + str(i + 1) + '.png') for i in range(2)]
    ghostD1 = [pg.image.load('images/GhostV' + str(i+1)+ '.png') for i in range(2)]
   
    dtimers = []
    timers = []

    dtimers.append(Timer(frames = ghostD1, wait = 300))
    timers.append(Timer(frames = ghost1, wait = 300))
    timers.append(Timer(frames = ghost2, wait = 300))
    timers.append(Timer(frames = ghost3, wait = 300))
    timers.append(Timer(frames = ghost4, wait = 300))

    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.settings.screen_width / 2, self.game.settings.screen_height / 2
        self.run_display = True
        self.cursor_rect = pg.Rect(0, 0, 20, 20)
        self.offset = - 100
        self.font_name = pg.font.get_default_font()
        self.sound = Sound(bg_music="sounds/pacman_beginning.wav")
        self.sound.play()
        #self.sound.pause_bg()

    def draw_cursor(self):
        self.draw_text('*', self.cursor_rect.x, self.cursor_rect.y)

    def draw_text(self, text, x, y):
        font = pg.font.Font(self.font_name, 20)
        text_surface = font.render(text, True, self.game.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.game.display.blit(text_surface, text_rect)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pg.display.update()
        self.game.reset_keys()

    
    def drawImage(self, x, y, image):
        rect = image.get_rect()
        rect.center = (x, y)
        self.game.display.blit(image, rect)


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Play"
        self.startx, self.starty = self.mid_w, self.mid_h + 100
        #add for other buttons here

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.blit(self.bgImg, (0, 0))
            self.drawImage(self.game.settings.screen_width / 2, self.game.settings.screen_height / 2, self.pacRAnim.imagerect())
            self.drawImage(self.game.settings.screen_width / 2 + 50, self.game.settings.screen_height / 2 - 50, self.timers[0].imagerect())
            self.drawImage(self.game.settings.screen_width / 2 - 50, self.game.settings.screen_height / 2 - 50, self.timers[1].imagerect())
            self.drawImage(self.game.settings.screen_width / 2 + 50, self.game.settings.screen_height / 2 + 50, self.timers[2].imagerect())
            self.drawImage(self.game.settings.screen_width / 2 - 50, self.game.settings.screen_height / 2 + 50, self.timers[3].imagerect())

            self.draw_text('Main Menu', self.game.settings.screen_width / 2, 40)
            self.draw_text("Play", self.startx, self.starty)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        #For Scroll Menu
        if self.state == 'Play':
            self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def check_input(self):
        self.move_cursor()

        if self.game.PLAY_KEY:
            if self.state == 'Play':
                self.game.finished = False
                self.game.reset_keys()
                self.run_display = False