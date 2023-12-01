import pygame
from pygame.locals import *
import gamebase

# constants
TICK_TIME = float(gamebase.TICK_TIME)

# init pygame
pygame.init()
screen = pygame.display.set_mode(gamebase.WINDOW_DIMENSION)
clock = pygame.time.Clock()

while True:
    request_quit = False

    # poll for events
    for event in pygame.event.get():
        if event.type == QUIT:
            request_quit = True
        gamebase.on_pygame_event(event)
    
    # handle quit request
    if request_quit:
        gamebase.on_quit()
        pygame.quit()
        break

    screen.fill(gamebase.BACKGROUND_COLOR)

    # tick time calculation and tick call
    dt = clock.tick(gamebase.TICK_RATE) / 1000
    gamebase.on_tick()
    latency = dt - TICK_TIME
    if latency > 0.005:
        print("WARNING: Performance issue. Latency: " + str(latency))
    
    pygame.display.flip()

    
    
    