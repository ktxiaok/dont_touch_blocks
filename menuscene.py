
from decimal import Decimal
import typing
from typing import Optional
from pygame import Surface
from basicscene import BasicScene
from player import PlayerInputManager
from scene import DynamicEntity
import gamebase
import gamesave


class MenuScene(BasicScene):
    
    def on_create(self):

        super().on_create()
        self.spawn_entity(Menu)

class Menu(DynamicEntity):
    
    __input_manager: PlayerInputManager

    __text_key_hint1: Surface
    __text_key_hint2: Surface
    __text_best_score: Optional[Surface] = None

    def on_spawn(self):

        super().on_spawn()
        self.__input_manager = typing.cast(
            PlayerInputManager, 
            self.scene.get_singleton_entity(PlayerInputManager)
        )
        font = gamebase.get_default_font()
        self.__text_key_hint1 = font.render(
            "Press Space to start the game!", True, "black"
        )
        self.__text_key_hint2 = font.render(
            "Press F to toggle fullscreen mode.", True, "black"
        )
        best_score = gamesave.get_best_score()
        if best_score != Decimal(0):
            self.__text_best_score = font.render(
                "Best Score: " + str(best_score), True, "orange"
            )
        
    def on_tick(self):

        screen = gamebase.get_screen()
        input_manager = self.__input_manager

        x = gamebase.WINDOW_DIMENSION[0] // 2
        y = 300
        screen.blit(
            self.__text_key_hint1, 
            (x - self.__text_key_hint1.get_width() // 2, y)
        )
        y += 60
        screen.blit(
            self.__text_key_hint2, 
            (x - self.__text_key_hint2.get_width() // 2, y)
        )
        y += 60
        text_best_score = self.__text_best_score
        if text_best_score != None:
            screen.blit(
                text_best_score,
                (x - text_best_score.get_width() // 2, y)
            )
        
        if input_manager.request_jump:
            gamebase.request_load_scene("GameScene")
        