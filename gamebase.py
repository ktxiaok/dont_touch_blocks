import decimal
from decimal import Decimal
import pygame

decimal.getcontext().prec = 6

# constants
WINDOW_DIMENSION = (1280, 720)
BACKGROUND_COLOR = 'white'

TICK_RATE = 64
TICK_TIME = Decimal(1) / Decimal(TICK_RATE)

def on_pygame_event(event: pygame.event.Event):
    pass

def on_quit():
    pass

def on_tick():
    pass