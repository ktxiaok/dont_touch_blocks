
import typing
from typing import Optional
import gamebase
import pygame
from pygame import Surface
from player import PlayerInputManager
from scene import DynamicEntity, Scene, SingletonEntity
import gamesave
from utils import FadeEffect

class BasicScene(Scene):

    def on_create(self):

        self.spawn_entity(DebugDisplay)
        self.spawn_entity(PlayerInputManager)
        self.spawn_entity(Caption)
        self.spawn_entity(KeyboardReactiveSettingsChanger)

    def on_destroy(self):

        pass

DEBUG_DISPLAY_POS_X = gamebase.WINDOW_DIMENSION[0]
DEBUG_DISPLAY_POS_Y = gamebase.WINDOW_DIMENSION[1] - 60

_debug_display_is_active: bool = False

class DebugDisplay(SingletonEntity, DynamicEntity):

    __last_frametime_ms: int = -1
    __frametime_surface: Optional[Surface] = None

    @property
    def is_active(self) -> bool:
        global _debug_display_is_active
        return _debug_display_is_active
    
    @is_active.setter
    def is_active(self, val: bool):
        global _debug_display_is_active
        _debug_display_is_active = val

    def on_late_tick(self):
        is_active = self.is_active
        if is_active:
            frametime_ms = gamebase.get_frametime_ms()
            if self.__last_frametime_ms != frametime_ms:
                self.__last_frametime_ms = frametime_ms
                font = gamebase.get_default_font()
                self.__frametime_surface = font.render(
                    f"frametime: {frametime_ms} ms", False, "khaki"
                )
        
            surface = self.__frametime_surface
            if surface != None:
                screen = gamebase.get_screen()
                screen.blit(
                    surface,
                    (DEBUG_DISPLAY_POS_X - surface.get_width(), DEBUG_DISPLAY_POS_Y)
                )
                        
    

CAPTION_POS_X = gamebase.WINDOW_DIMENSION[0] // 2
CAPTION_POS_Y = gamebase.WINDOW_DIMENSION[1] - 200
CAPTION_FADE_TIME = 0.5
CAPTION_HOLD_TIME = 1.0

class Caption(SingletonEntity, DynamicEntity):

    __surface: Optional[Surface] = None
    __fade_effect: FadeEffect

    def set_surface(self, parent_surface: Surface):
        self.__surface = parent_surface.subsurface(
            (0, 0), parent_surface.get_size()
        )
        self.__fade_effect = FadeEffect(
            CAPTION_FADE_TIME, CAPTION_HOLD_TIME, CAPTION_FADE_TIME
        )

    def on_late_tick(self):
        
        surface = self.__surface
        if surface != None:
            dt = gamebase.TICK_TIME_FLOAT
            fade_effect = self.__fade_effect
            fade_effect.update(dt)
            if fade_effect.is_finished:
                self.__surface = None
                self.__fade_effect = None # type:ignore
            else:
                screen = gamebase.get_screen()
                surface.set_alpha(int(255 * fade_effect.value))
                screen.blit(
                    surface, 
                    (CAPTION_POS_X - surface.get_width() // 2, CAPTION_POS_Y)
                )

FONT = gamebase.get_default_font()

def _generate_bool_option_imgs(name: str):
    return {
        enabled : FONT.render(f"{name} {"Enabled" if enabled else "Disabled"}", True, "black") for enabled in (True, False)
    }

IMGS_FULLSCREEN_SWITCH = _generate_bool_option_imgs("Fullscreen")
IMGS_MUTE_SWITCH = _generate_bool_option_imgs("Mute")

class KeyboardReactiveSettingsChanger(DynamicEntity):

    __input_manager: PlayerInputManager

    __debug_display: DebugDisplay

    __caption: Caption
    
    def on_spawn(self):

        super().on_spawn()
        self.__input_manager = typing.cast(
            PlayerInputManager, 
            self.scene.get_singleton_entity(PlayerInputManager)
        )
        self.__debug_display = typing.cast(
            DebugDisplay, self.scene.get_singleton_entity(DebugDisplay)
        )
        self.__caption = typing.cast(
            Caption, self.scene.get_singleton_entity(Caption)
        )

        if gamesave.get("is_fullscreen", bool) ^ pygame.display.is_fullscreen():
            pygame.display.toggle_fullscreen()

    def on_tick(self):
        
        input_manager = self.__input_manager
        if input_manager.request_debug:
            debug_display = self.__debug_display
            debug_display.is_active = not debug_display.is_active
        if input_manager.request_fullscreen:
            pygame.display.toggle_fullscreen()
            is_fullscreen = pygame.display.is_fullscreen()
            gamesave.set("is_fullscreen", is_fullscreen)
            self.__caption.set_surface(IMGS_FULLSCREEN_SWITCH[is_fullscreen])
        if input_manager.request_mute:
            is_mute = gamesave.get("is_mute", bool)
            is_mute = not is_mute
            gamesave.set("is_mute", is_mute)
            self.__caption.set_surface(IMGS_MUTE_SWITCH[is_mute])