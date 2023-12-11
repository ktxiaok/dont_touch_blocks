'''
This is the basic framework of the entire game program. 
'''

from typing import Type, Optional
import decimal
from decimal import Decimal
import pygame
from pygame.locals import *
from pygame import display
from scene import Scene
from utils import InvalidOperationException

decimal.getcontext().prec = 5

# constants
WINDOW_DIMENSION = (1280, 800)
BACKGROUND_COLOR = 'white'

TICK_RATE = 100
TICK_TIME = Decimal(1) / Decimal(TICK_RATE)
TICK_TIME_FLOAT = float(TICK_TIME)

GRAVITY_ACCEL = Decimal(1000)

PRINT_INTERVAL = 50

_screen: pygame.Surface

_active_scene: "Scene" = None # type:ignore

_scene_type_to_load: Optional[Type["Scene"]] = None 

def get_screen():
    '''
    A pygame.Surface instance representing the main window.
    '''

    global _screen
    return _screen

def get_active_scene():
    '''
    A Scene instance representing the current active game scene.
    '''

    global _active_scene
    return _active_scene

def request_load_scene(scene_type: Type["Scene"]):
    '''
    Request to destroy current scene and load a new scene.
    
    Args:
        scene_type: The class object of the scene to load.

    Raises:
        ValueError: The argument type is not correct.
        TypeError: Arg scene_type is not the subclass of Scene.
        InvalidOperationException: There is already a scene ready to load.
    '''

    global _scene_type_to_load
    if not isinstance(scene_type, type):
        raise ValueError("Arg scene_type must be a type object!")
    if not issubclass(scene_type, Scene):
        raise TypeError("Arg scene_type must be the subclass of Scene!")
    if _scene_type_to_load != None:
        raise InvalidOperationException("There is already a scene ready to load!")
    
    _scene_type_to_load = scene_type

def run(initial_scene_type: Type["Scene"]):
    '''
    Run the game!

    There's a game loop inside this function. The game updates a frame at set intervals. This function will exit when a quit event occurs.

    Args:
        initial_scene_type: The type of the first Scene instance the game will create.

    Raises:
        ValueError: The argument type is not correct.
        TypeError: Arg initial_scene_type is not the subclass of Scene. 
    '''

    global _screen
    global _active_scene
    global _scene_type_to_load

    request_load_scene(initial_scene_type)
    
    # init pygame
    pygame.init()
    _screen = display.set_mode(WINDOW_DIMENSION)
    clock = pygame.time.Clock()
    request_quit = False
    print_timer = PRINT_INTERVAL

    while True:
        # check whether there's a request to load a new scene.
        if _scene_type_to_load != None:
            if _active_scene != None: 
                _active_scene.on_destroy()
            _active_scene = _scene_type_to_load()
            _active_scene.on_create()
            _scene_type_to_load = None
        
        # poll for events
        for event in pygame.event.get():
            if event.type == QUIT:
                request_quit = True
            _active_scene._send_pygame_event(event)
        
        # handle the quit request
        if request_quit:
            _active_scene.on_destroy()
            pygame.quit()
            break

        _screen.fill(BACKGROUND_COLOR)

        # tick time calculation and tick call
        dt = clock.tick_busy_loop(TICK_RATE) / 1000
        _active_scene._tick()
        latency = dt - TICK_TIME_FLOAT
        if latency > 0.005:
            print_timer += 1
            if print_timer > PRINT_INTERVAL:
                print_timer = 0
                print(f"WARNING: Performance issue. Latency: {latency}")
        
        display.flip()