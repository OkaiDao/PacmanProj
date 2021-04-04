import pygame as pg

class Sound:
    def __init__(self, bg_music):
        pg.mixer.init()
        pg.mixer.music.load(bg_music)
        pg.mixer.music.set_volume(0.5)

        chomp = pg.mixer.Sound('sounds/pacman_chomp.wav')
        pg.mixer.Sound.set_volume(chomp, 0.22)

        fruit = pg.mixer.Sound('sounds/pacman_eatfruit.wav')
        pg.mixer.Sound.set_volume(fruit, 0.22)

        ghost = pg.mixer.Sound('sounds/pacman_eatghost.wav')
        pg.mixer.Sound.set_volume(ghost, 0.22)

        death = pg.mixer.Sound('sounds/pacman_death.wav')
        pg.mixer.Sound.set_volume(death, 0.22)

        self.sounds = {'chomp': chomp, 'fruit': fruit, 'ghost': ghost, 'death': death}
        self.playing_bg = None
        self.play()
        self.pause_bg()

    def pause_bg(self):
        self.playing_bg = False
        pg.mixer.music.pause()

    def unpause_bg(self):
        self.playing_bg = True
        pg.mixer.music.unpause()

    def play(self):
        self.playing_bg = True
        pg.mixer.music.play(-1, 0.0)

    def stop_bg(self):
        self.playing_bg = False
        pg.mixer.music.stop()

    def chomp(self): 
        pg.mixer.Sound.play(self.sounds['chomp'])

    def fruit(self): 
        pg.mixer.Sound.play(self.sounds['fruit'])

    def ghost(self):
        pg.mixer.Sound.play(self.sounds['ghost'])

    def death(self):
        pg.mixer.Sound.play(self.sounds['death'])

