'''
This module contains entities about player.
'''

from decimal import Decimal
import decimal
import blockmap
from blockmap import BlockMapManager
import gamebase
from scene import Scene, DynamicEntity, PygameEventListenerEntity, SingletonEntity
import pygame
from pygame import draw

class PlayerInputManager(SingletonEntity, PygameEventListenerEntity):
    
    __request_jump: bool = False

    @property
    def request_jump(self) -> bool:
        result = self.__request_jump
        self.__request_jump = False
        return result

    def on_pygame_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                self.__request_jump = True
            
PLAYER_JUMP_SPEED = Decimal(300)
PLAYER_OFFSET_X = 200
PLAYER_INITIAL_POS_Y = Decimal(200)
PLAYER_RADIUS = 20

class Player(SingletonEntity, DynamicEntity):

    __input_manager: PlayerInputManager
    __blockmap_manager: BlockMapManager

    __pos_y: Decimal = PLAYER_INITIAL_POS_Y
    __speed_y: Decimal = Decimal(0)

    __is_dead: bool = False

    @property
    def is_dead(self) -> bool:
        return self.__is_dead
    
    def on_spawn(self):
        super().on_spawn()
        self.__input_manager = self.scene.get_singleton_entity(
            PlayerInputManager) #type:ignore
        self.__blockmap_manager = self.scene.get_singleton_entity(
            BlockMapManager) #type:ignore
        
    def __move(self, dt: Decimal):
        input_manager = self.__input_manager
        if input_manager.request_jump:
            self.__speed_y = -PLAYER_JUMP_SPEED
        g_accel = gamebase.GRAVITY_ACCEL
        self.__speed_y += g_accel * dt 
        self.__pos_y += self.__speed_y * dt
        
        y = self.__pos_y
        if y < 0 or y > blockmap.BLOCK_MAP_SURFACE_HEIGHT or self.__blockmap_manager.test_touch_block(Decimal(PLAYER_OFFSET_X), y):
            self.__is_dead = True
    
    def on_tick(self):
        dt = gamebase.TICK_TIME
        screen = gamebase.get_screen()
        is_dead = self.__is_dead
        if not is_dead:
            self.__move(dt)
        draw.circle(
            screen, "blue" if not is_dead else "red", (PLAYER_OFFSET_X, int(self.__pos_y)), PLAYER_RADIUS)
