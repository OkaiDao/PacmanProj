import pygame as pg
from pygame.sprite import Sprite
from timer import Timer      

class Pacman:

    pacR = [pg.image.load('images/PacR.png'), pg.image.load('images/PacRO.png')]
    pacL = [pg.image.load('images/PacL.png'), pg.image.load('images/PacLO.png')]
    pacU = [pg.image.load('images/PacU.png'), pg.image.load('images/PacUO.png')]
    pacD = [pg.image.load('images/PacD.png'), pg.image.load('images/PacDO.png')]

    pacR =[pg.transform.rotozoom(pacR[0], 0, .8), pg.transform.rotozoom(pacR[1], 0, .8)]
    pacL =[pg.transform.rotozoom(pacL[0], 0, .8), pg.transform.rotozoom(pacL[1], 0, .8)]
    pacU =[pg.transform.rotozoom(pacU[0], 0, .8), pg.transform.rotozoom(pacU[1], 0, .8)]
    pacD =[pg.transform.rotozoom(pacD[0], 0, .8), pg.transform.rotozoom(pacD[1], 0, .8)]

    pacRAnim = Timer(frames = pacR, wait = 200)
    pacLAnim = Timer(frames = pacR, wait = 200)
    pacUAnim = Timer(frames = pacR, wait = 200)
    pacDAnim = Timer(frames = pacR, wait = 200)

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.pacRect = self.pacR[0].get_rect()
        self.dirR = True
        self.dirL, self.dirU, self.dirD = False, False, False

        self.pacRect.centerx, self.pacRect.bottom = self.screen_rect.centerx, self.screen_rect.bottom - 31

    def update(self):
        detla = self.settings.pacSpeed
        self.draw()

    def draw(self):
        if self.dirR: image = self.pacRAnim.imagerect()
        if self.dirL: image = self.pacLAnim.imagerect()
        if self.dirU: image = self.pacUAnim.imagerect()
        if self.dirD: image = self.pacDAnim.imagerect()

        rect = image.get_rect()
        rect.x, rect.y = self.pacRect.x, self.pacRect.y
        self.screen.blit(image, rect)