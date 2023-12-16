'''
This is the basic framework of the entire game program. 
'''

from typing import Dict, Type, Optional
import decimal
from decimal import Decimal
import pygame
from pygame import display
from pygame.font import Font
from scene import Scene
from utils import InvalidOperationException
import gamesave
import gc

pygame.init()

gamesave.load()

decimal.getcontext().prec = 5

# constants
WINDOW_DIMENSION = (1280, 800)
BACKGROUND_COLOR = (205, 201, 201)

TICK_RATE = 100
TICK_TIME = Decimal(1) / Decimal(TICK_RATE)
TICK_TIME_FLOAT = float(TICK_TIME)

GRAVITY_ACCEL = Decimal(1000)

PRINT_INTERVAL = 50

_screen: pygame.Surface

_default_font: Font = Font(None, size = 50)
_default_font.set_bold(True)

_active_scene: "Scene" = None # type:ignore

_scene_type_to_load: Optional[Type["Scene"]] = None 

_scene_type_dict: Dict[str, Type["Scene"]] = {}

def get_screen():
    '''
    A pygame.Surface instance representing the main window.
    '''

    global _screen
    return _screen

def get_default_font():
    '''
    Returns a default pygame.font.Font instance.
    '''

    global _default_font
    return _default_font

def get_active_scene():
    '''
    A Scene instance representing the current active game scene.
    '''

    global _active_scene
    return _active_scene

def register_scene(name: str, scene_type: Type["Scene"]):
    '''
    Register a scene type.

    Args:
        name: The scene name to register.
        scene_type: The scene type object to register.
    '''

    global _scene_type_dict

    _scene_type_dict[name] = scene_type

def request_load_scene(name: str):
    '''
    Request to destroy current scene and load a new scene.
    
    Args:
        name: The registered scene name to load.

    Raises:
        InvalidOperationException: There is already a scene ready to load.
    '''

    global _scene_type_to_load
    global _scene_type_dict

    if _scene_type_to_load != None:
        raise InvalidOperationException("There is already a scene ready to load!")
    
    _scene_type_to_load = _scene_type_dict[name]

def run(initial_scene_name: str):
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

    request_load_scene(initial_scene_name)
    
    # init
    _screen = display.set_mode(WINDOW_DIMENSION, vsync = 1)
    display.set_caption("Don't Touch Blocks")
    clock = pygame.time.Clock()
    request_quit = False
    print_timer = PRINT_INTERVAL

    while True:
        # check whether there's a request to load a new scene.
        if _scene_type_to_load != None:
            if _active_scene != None: 
                _active_scene._destroy()
            _active_scene = _scene_type_to_load()
            _active_scene.on_create()
            _scene_type_to_load = None
            gc.collect()
        
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
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