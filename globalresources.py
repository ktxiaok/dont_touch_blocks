import pygame
from pygame.mixer import Sound

SND_JUMP: Sound
SND_DEAD: Sound
SND_NEW_BEST_SCORE: Sound

def _load():
    global SND_JUMP
    global SND_DEAD
    global SND_NEW_BEST_SCORE

    SND_JUMP = Sound("resources/193438__unfa__jumping.ogg")
    SND_DEAD = Sound("resources/483598__raclure__wrong.mp3")
    SND_NEW_BEST_SCORE = Sound("resources/588234__mehraniiii__win.ogg")
