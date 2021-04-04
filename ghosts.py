import pygame as pg
from pygame.sprite import Sprite
from timer import Timer

class Ghost(Sprite):
    ghost1 = [pg.image.load('images/Ghost1_' + str(i + 1) + '.png') for i in range(2)]
    ghost2 = [pg.image.load('images/Ghost2_' + str(i + 1) + '.png') for i in range(2)]
    ghost3 = [pg.image.load('images/Ghost3_' + str(i + 1) + '.png') for i in range(2)]
    ghost4 = [pg.image.load('images/Ghost4_' + str(i + 1) + '.png') for i in range(2)]

    ghost1 = [pg.transform.rotozoom(ghost1[0], 0, .8), pg.transform.rotozoom(ghost1[1], 0, .8)]
    ghost2 = [pg.transform.rotozoom(ghost2[0], 0, .8), pg.transform.rotozoom(ghost2[1], 0, .8)]
    ghost3 = [pg.transform.rotozoom(ghost3[0], 0, .8), pg.transform.rotozoom(ghost3[1], 0, .8)]
    ghost4 = [pg.transform.rotozoom(ghost4[0], 0, .8), pg.transform.rotozoom(ghost4[1], 0, .8)]

    timers = []
    timers.append(Timer(frames = ghost1, wait = 300))
    timers.append(Timer(frames = ghost2, wait = 300))
    timers.append(Timer(frames = ghost3, wait = 300))
    timers.append(Timer(frames = ghost4, wait = 300))

    def __init__(self, game, number, x, y):
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.timer = Ghost.timers[number]
        self.rect = self.timer.imagerect().get_rect()
        self.rect.x = self.x = x
        self.rect.y = self.y = y
        self.x = float(self.rect.x)
        self.rect.centerx, self.rect.centery = self.screen_rect.centerx + x, self.screen_rect.centery + y

    def update(self):
        delta = self.settings.ghostSpeed
        r = self.screen_rect
        self.draw()


    def draw(self):
        image = self.timer.imagerect()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)

