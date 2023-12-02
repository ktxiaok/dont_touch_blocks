import decimal
from decimal import Decimal
import pygame
from pygame.locals import *
from pygame import display

decimal.getcontext().prec = 6

# constants
WINDOW_DIMENSION = (1280, 720)
BACKGROUND_COLOR = 'white'

TICK_RATE = 100
TICK_TIME = Decimal(1) / Decimal(TICK_RATE)
TICK_TIME_FLOAT = float(TICK_TIME)

_screen = None

def run():
    global _screen
    
    # init pygame
    pygame.init()
    _screen = display.set_mode(WINDOW_DIMENSION)
    clock = pygame.time.Clock()

    while True:
        request_quit = False

        # poll for events
        for event in pygame.event.get():
            if event.type == QUIT:
                request_quit = True
            on_pygame_event(event)
        
        # handle quit request
        if request_quit:
            on_quit()
            pygame.quit()
            break

        _screen.fill(BACKGROUND_COLOR)

        # tick time calculation and tick call
        dt = clock.tick(TICK_RATE) / 1000
        on_tick()
        latency = dt - TICK_TIME_FLOAT
        if latency > 0.005:
            print("WARNING: Performance issue. Latency: " + str(latency))
        
        display.flip()

def on_pygame_event(event: pygame.event.Event):
    pass

def on_quit():
    pass

def on_tick():
    from _test import test1
    test1.update(_screen, float(TICK_TIME))