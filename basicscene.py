
import typing

import pygame
from player import PlayerInputManager
from scene import DynamicEntity, Scene
import gamesave


class BasicScene(Scene):

    def on_create(self):

        self.spawn_entity(PlayerInputManager)
        self.spawn_entity(FullscreenSwitcher)

    def on_destroy(self):

        pass

class FullscreenSwitcher(DynamicEntity):

    __input_manager: PlayerInputManager
    
    def on_spawn(self):

        super().on_spawn()
        self.__input_manager = typing.cast(
            PlayerInputManager, 
            self.scene.get_singleton_entity(PlayerInputManager)
        )

        if gamesave.get("is_fullscreen", bool) ^ pygame.display.is_fullscreen():
            pygame.display.toggle_fullscreen()

    def on_tick(self):
        
        input_manager = self.__input_manager
        if input_manager.request_fullscreen:
            pygame.display.toggle_fullscreen()
            gamesave.set("is_fullscreen", pygame.display.is_fullscreen())