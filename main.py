import pygame
from pygame.locals import *
import gamebase

# constants
MAX_TICK_COUNT_PER_FRAME = 4
TICK_TIME = float(gamebase.TICK_TIME)

# init pygame
pygame.init()
screen = pygame.display.set_mode(gamebase.WINDOW_DIMENSION)
clock = pygame.time.Clock()
delta_time = 0.0
tick_timer = 0.0

while True:
    request_quit = False

    # poll for events
    for event in pygame.event.get():
        if event.type == QUIT:
            request_quit = True
        gamebase.on_event(event)
    
    # handle quit request
    if request_quit:
        gamebase.on_quit()
        pygame.quit()
        break

    screen.fill(gamebase.BACKGROUND_COLOR)
    pygame.display.flip()

    # game delta time(mainly for rendering) and tick time(mainly for game logic) calculation
    delta_time = clock.tick(gamebase.TICK_RATE) / 1000
    gamebase.on_update(delta_time)
    tick_timer += delta_time
    tick_count = 0
    while tick_timer >= TICK_TIME:
        tick_timer -= TICK_TIME
        gamebase.on_tick()
        tick_count += 1
        # avoid death spiral
        if tick_count >= MAX_TICK_COUNT_PER_FRAME:
            break

    
    
    