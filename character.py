import pygame as pg
from math import atan2
from copy import copy
from vector import Vector
from timer import Timer
from settings import Settings
from random import seed
from random import randint
from math import fabs

def compare(a, b): return fabs(a - b) < epsilon
epsilon = 0.0001

class Character:
    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev, name, number, image, scale):
        self.game = game
        self.screen, self.screen_rect = game.screen, game.screen.get_rect()
        self.name = name
        self.grid_pt, self.grid_pt_next, self.grid_pt_prev = grid_pt, grid_pt_next, grid_pt_prev

        pt_next = self.grid_pt_next.pt
        self.pt = copy(self.grid_pt.pt)
        delta = pt_next - self.pt
        v = delta.normalize()
        self.grid_pt_next.make_next()
        self.grid_pt_prev.make_prev()
        self.number = number
        self.timedImage = image
        self.timer = self.timedImage[number]
        self.image = self.timer.imagerect()
        self.scale = scale
        self.origimage = self.image
        self.scale_factor = 1.0
        self.v = v
        self.prev_angle = 90.0
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        self.prev_angle = curr_angle
        #print(f'>>>>>>>>>>>>>>>>>>>>>>>> PREV ANGLE is {self.prev_angle}')
        self.last = self.grid_pt
        if self.grid_pt_prev is None: print("PT_PREV IS NONE NONE NONE NONE NONE")
        self.image = pg.transform.rotozoom(self.image, delta_angle, scale)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.printed = False

    def clamp(self):
        screen = self.screen_rect
        self.pt.x = max(0, min(self.pt.x, screen.width))
        self.pt.y = max(0, min(self.pt.y, screen.height))

    def enterPortal(self): pass

    def at_dest(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2:
            self.grid_pt = self.grid_pt_next
            self.pt = self.grid_pt.pt
            newdelta = self.pt - self.grid_pt_next.pt
            if not self.printed:
                print(f'newdelta is: {newdelta} and mag is {newdelta.magnitude()}')
                print(f'AT DEST {self.grid_pt.index} delta is {delta} pt is {self.pt}, next is {self.grid_pt_next.pt} with adj_list {self.grid_pt.adj_list}')
                self.printed = True
            return True
        return False

    def at_source(self):
        delta = (self.pt - self.grid_pt_next.pt).magnitude()
        if delta < 2 and delta > 0.1:
            self.pt = self.grid_pt_next.pt
            print(f'AT SOURCE {self.grid_pt.index} with adj_list {self.grid_pt.adj_list}')
            return True
        return False

    def on_star(self):
        return self.at_dest() or self.at_source()

    def to_grid(self, index):
        return self.game.to_grid(index)

    def update_next_prev(self):
        self.grid_pt_next.make_next()
        self.grid_pt_prev.make_visited()

    def reverse(self):
        temp = self.grid_pt_prev
        self.grid_pt_prev = self.grid_pt_next
        self.grid_pt_next = temp

        self.grid_pt_prev.make_prev()
        self.grid_pt_next.make_next()

        self.v *= -1
        self.scale_factor = 1
        self.update_angle()

    def angle(self):
        return round((atan2(self.v.x, self.v.y) * 180.0 / 3.1415 - 90) % 360, 0)
        # return atan2(self.v.x, self.v.y) * 180.0 / 3.1415 + 180.0

    def update_angle(self):
        curr_angle = self.angle()
        delta_angle = curr_angle - self.prev_angle
        # self.image = pg.transform.rotozoom(self.image, delta_angle, 1.0)
        self.image = pg.transform.rotozoom(self.origimage, curr_angle - 90.0, self.scale)
        self.prev_angle = curr_angle

    def update(self):
        # print(f'{self.pt} with dims={self.pt.dims} and {self.pt_next} with dims={self.pt.dims}')
        delta = self.pt - self.grid_pt_next.pt
        # print(f'         delta is: {delta} and mag is {delta.magnitude()}')
        if self.at_dest():   
            self.draw();  return

        print(f'changing location... --- with velocity {self.v}')
            # print(f'current {self.grid_pt}... --- next {self.grid_pt_next}')
            # self.prev = self.grid_pt
        self.printed = False
        self.pt += self.scale_factor * self.v
        self.clamp()
        if self.grid_pt != self.last:
            # print(f'{self.name}@{self.pt} -- next is: {self.grid_pt_next}')
            self.last = self.grid_pt
        self.rect.centerx, self.rect.centery = self.pt.x, self.pt.y
        self.draw()

    def draw(self):
        image = self.timer.imagerect()
        #self.rect = image.get_rect()
        self.screen.blit(image, self.rect)


class Pacman(Character):
    pacR = [pg.image.load('images/PacR.png'), pg.image.load('images/PacRO.png')]
#    pacL = [pg.image.load('images/PacL.png'), pg.image.load('images/PacLO.png')]
#    pacU = [pg.image.load('images/PacU.png'), pg.image.load('images/PacUO.png')]
#    pacD = [pg.image.load('images/PacD.png'), pg.image.load('images/PacDO.png')]

    pacR =[pg.transform.rotozoom(pacR[0], 0, .5), pg.transform.rotozoom(pacR[1], 0, .5)]
#    pacL =[pg.transform.rotozoom(pacL[0], 0, .8), pg.transform.rotozoom(pacL[1], 0, .8)]
#    pacU =[pg.transform.rotozoom(pacU[0], 0, .8), pg.transform.rotozoom(pacU[1], 0, .8)]
#    pacD =[pg.transform.rotozoom(pacD[0], 0, .8), pg.transform.rotozoom(pacD[1], 0, .8)]

    pacRAnim = []
    pacRAnim.append(Timer(frames = pacR, wait = 300))

#    pacRAnim = Timer(frames = pacR, wait = 200)
#    pacLAnim = Timer(frames = pacR, wait = 200)
#    pacUAnim = Timer(frames = pacR, wait = 200)
#    pacDAnim = Timer(frames = pacR, wait = 200)

    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev, name="Pacman", number = 0, pacR = pacRAnim, scale=0.55):
        super().__init__(game=game, name=name, number=number, image = pacR, scale=scale,
                         v=v, grid_pt=grid_pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev)

        self.dirL, self.dirU, self.dirD = False, False, False
        self.strt_PT = grid_pt
        self.strt_Next = grid_pt_next
        self.strt_Prev = grid_pt_prev
        self.dead = False
        self.port1 = False
        self.port1loc = self.grid_pt
        self.port2loc = self.grid_pt
        self.port2 = False

    def killGhost(self):
        game.score += 100

    def eatPoint(self):
        game.score += 5

    def eatFruit(self):
        game.score += 15

    def eatPowerPill(self):
        game.PowerPhase = True

    def firePortalGun(self):
        if not self.port1:
            self.placePortal()
            self.port1 = True
        if self.port1 and not self.port2:
            self.placePortal()
            self.port2 = True

    def die(self):
        self.grid_pt = self.strt_PT
        self.grid_pt_next = self.strt_Next
        self.grid_pt_prev = self.strt_Prev

    def placePortal(self):
        image = pg.image.load('images/portal1.png')
        image2 = pg.image.load('images/portal2.png')
        rect = image.get_rect()
        rect.centerx, rect.centery = self.pt.x, self.pt.y    
        rect2 = image2.get_rect()
        rect2.centerx, rect2.centery = self.pt.x, self.pt.y    

        if not self.port1:
            self.screen.blit(image, rect)
            self.port1 = True
            self.port1loc = self.grid_pt
        elif self.port1 and not self.port2:
            self.screen.blit(image2, rect2)
            self.port2 = True
            self.port2loc = self.grid_pt

    def checkEnter(self):
        if port1 and port2:
            if self.grid_pt == port1Loc:
                self.grid_pt == port2loc
            elif self.grid_pt == port2Loc:
                self.grid_pt == port1Loc

class Ghost(Character):

    ghost1 = [pg.image.load('images/Ghost1_' + str(i + 1) + '.png') for i in range(2)]
    ghost2 = [pg.image.load('images/Ghost2_' + str(i + 1) + '.png') for i in range(2)]
    ghost3 = [pg.image.load('images/Ghost3_' + str(i + 1) + '.png') for i in range(2)]
    ghost4 = [pg.image.load('images/Ghost4_' + str(i + 1) + '.png') for i in range(2)]

    ghost1 = [pg.transform.rotozoom(ghost1[0], 0, .8), pg.transform.rotozoom(ghost1[1], 0, .8)]
    ghost2 = [pg.transform.rotozoom(ghost2[0], 0, .8), pg.transform.rotozoom(ghost2[1], 0, .8)]
    ghost3 = [pg.transform.rotozoom(ghost3[0], 0, .8), pg.transform.rotozoom(ghost3[1], 0, .8)]
    ghost4 = [pg.transform.rotozoom(ghost4[0], 0, .8), pg.transform.rotozoom(ghost4[1], 0, .8)]

    ghostD1 = [pg.image.load('images/GhostV' + str(i+1)+ '.png') for i in range(2)]
    ghostD1 = [pg.transform.rotozoom(ghostD1[0], 0, .8), pg.transform.rotozoom(ghostD1[1], 0, .8)]

    dtimers = []
    timers = []

    dtimers.append(Timer(frames = ghostD1, wait = 300))
    timers.append(Timer(frames = ghost1, wait = 300))
    timers.append(Timer(frames = ghost2, wait = 300))
    timers.append(Timer(frames = ghost3, wait = 300))
    timers.append(Timer(frames = ghost4, wait = 300))
    seed(1)

    def __init__(self, game, v, grid_pt, grid_pt_next, grid_pt_prev, name, number, ghost = timers, scale = 0.8):
        super().__init__(game, name=name, number=number, image = ghost, scale=scale, 
                         v=v, grid_pt=grid_pt, grid_pt_next=grid_pt_next, grid_pt_prev=grid_pt_prev)
        self.strt_PT = grid_pt
        self.strt_Next = grid_pt_next
        self.strt_Prev = grid_pt_prev
        self.vuln = False
        self.timers = Ghost.timers
        self.dtimers = Ghost.dtimers
        self.Occupied = 0
        self.spawned = False

    def switchToChase(self):
        self.timedImage = Ghost.timers
        self.timer = self.timedImage[self.number]
        self.image = self.timer.imagerect()
        self.vuln = False

    def switchToRun(self):
        self.timedImage = Ghost.dtimers
        self.timer = self.timedImage[0]
        self.image = self.timer.imagerect()
        self.vuln = True

    def spawnOut(self):
        self.grid_pt = self.game.maze.location(6,5)
        self.grid_pt_next = self.game.maze.location(6,4)
        self.grid_pt_prev = self.game.maze.location(6,6)
        self.game.occupied -=1
        self.Occupied = 0
        self.spawned = True

    def die(self):
        self.spawned = False

        if self.game.occupied == 3:
            self.spawnOut()
        elif self.game.occupied == 2:
            self.grid_pt = self.game.maze.location(5,4)
            self.grid_pt_next = self.game.maze.location(5,6)
            self.grid_pt_prev = self.game.maze.location(5,5)
            self.Occupied = 3
        elif self.game.occupied == 1:
            self.grid_pt = self.game.maze.location(5,6)
            self.grid_pt_next = self.game.maze.location(5,5)
            self.grid_pt_prev = self.game.maze.location(5,4)
            self.Occupied = 2
        elif self.game.occupied == 0:
            self.grid_pt = self.game.maze.location(5,5)
            self.grid_pt_next = self.game.maze.location(5,4)
            self.grid_pt_prev = self.game.maze.location(5,6)
            self.Occupied = 1

        self.game.occupied +=1

    def move(self):
        new_dir = self.genDirection()

        if self.on_star():
            delta = (self.v.x if self.v.y == 0 else -11 * self.v.y)
            idx = self.grid_pt.index
            possible_idx = idx + int(delta)
            if possible_idx in self.grid_pt.adj_list:
                self.grid_pt_prev.make_normal()
                self.grid_pt_next = self.to_grid(possible_idx)
                self.grid_pt_prev = self.grid_pt
                self.update_next_prev()

            self.v = new_dir
            self.scale_factor = 1.0
            self.update_angle()


    def genDirection(self):
        rNum = randint(0,3)

        if rNum == 0:
            new_dir = Vector(1,0)
        elif rNum == 1:
            new_dir = Vector(-1,0)
        elif rNum == 2:
            new_dir = Vector(0,-1)
        else:
            new_dir = Vector(0,1)
        return new_dir


