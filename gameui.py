'''
This module is mainly about the UI in game.
'''

from decimal import Decimal
from typing import Optional
import typing
from pygame import Color, Surface
import pygame
import gamebase
from gamerule import GameRule
from player import PlayerInputManager
from scene import DynamicEntity
import globalresources
import gamesave

FONT_HEIGHT = gamebase.get_default_font().get_height()
SCORE_COLOR = Color("yellow")
SPEED_COLOR = Color("aqua")
GAMEOVER_COLOR = Color("red")
BEST_SCORE_COLOR = Color("orange")
NEW_BEST_SCORE_COLOR = Color("chartreuse")
MASK_COLOR = Color(100, 100, 100)
SCORE_POS_X = gamebase.WINDOW_DIMENSION[0] // 2 - 100
SCORE_POS_Y = 50
SPEED_POS_X = SCORE_POS_X
SPEED_POS_Y = SCORE_POS_Y + FONT_HEIGHT + 10
GAMEOVER_POS_X = gamebase.WINDOW_DIMENSION[0] // 2
GAMEOVER_POS_Y = 300
GAMEOVER_SCORE_POS_X = GAMEOVER_POS_X
GAMEOVER_SCORE_POS_Y = GAMEOVER_POS_Y + FONT_HEIGHT + 15
GAMEOVER_SPEED_POS_X = GAMEOVER_SCORE_POS_X
GAMEOVER_SPEED_POS_Y = GAMEOVER_SCORE_POS_Y + FONT_HEIGHT + 10
GAMEOVER_BEST_SCORE_POS_X = GAMEOVER_POS_X
GAMEOVER_BEST_SCORE_POS_Y = GAMEOVER_SPEED_POS_Y + FONT_HEIGHT + 10
GAMEOVER_KEY_HINT_POS_X = GAMEOVER_POS_X
GAMEOVER_KEY_HINT_POS_Y = GAMEOVER_BEST_SCORE_POS_Y + FONT_HEIGHT + 15
GAMEOVER_ACCEPT_KEY_TIME = 1.0

class GameUi(DynamicEntity):
    '''
    This class is responsible for displaying score, player speed, menus and so on. 
    '''

    __game_rule: GameRule
    __player_input_manager: PlayerInputManager

    __last_score: Decimal = Decimal("0.0")
    __last_text_score: Optional[Surface] = None
    __last_speed: Decimal = Decimal("0.0")
    __last_text_speed: Optional[Surface] = None

    __text_gameover: Surface
    __text_gameover_key_hint: Surface
    __text_best_score: Surface

    __gameover_accept_key_timer: float = 0.0
    __gameover_accept_key: bool = False

    __on_gameover_called: bool = False

    def on_spawn(self):
        
        super().on_spawn()
        self.__game_rule = typing.cast(
            GameRule, self.scene.get_singleton_entity(GameRule)
        )
        self.__player_input_manager = typing.cast(
            PlayerInputManager, 
            self.scene.get_singleton_entity(PlayerInputManager)
        )
        font = gamebase.get_default_font()
        self.__text_gameover = font.render("GAME OVER", True, GAMEOVER_COLOR)
        self.__text_gameover_key_hint = font.render(
            "Press Space to play again or Esc to exit.", True, "white"
        )

    def on_tick(self):

        game_rule = self.__game_rule
        if game_rule.is_game_over:
            if not self.__on_gameover_called:
                self.__on_gameover_called = True
                self.__on_game_over()
            self.__tick_game_over()
        else:
            self.__tick_during_game()
    
    def __update_score(self):
        game_rule = self.__game_rule
        font = gamebase.get_default_font()
        score = game_rule.score.quantize(Decimal("1.0"))
        if score != self.__last_score:
            self.__last_score = score
            self.__last_text_score = font.render(
                "Score: " + str(score), True, SCORE_COLOR
            )

    def __update_speed(self):
        game_rule = self.__game_rule
        font = gamebase.get_default_font()
        speed = game_rule.player_speed.quantize(Decimal("1.0"))
        if speed != self.__last_speed:
            self.__last_speed = speed
            self.__last_text_speed = font.render(
                "Speed: " + str(speed), True, SPEED_COLOR
            )

    def __tick_during_game(self):

        screen = gamebase.get_screen()

        self.__update_score()
        text_score = self.__last_text_score
        if text_score != None:
            screen.blit(
                text_score, (SCORE_POS_X, SCORE_POS_Y)
            )
        
        self.__update_speed()
        text_speed = self.__last_text_speed
        if text_speed != None:
            screen.blit(
                text_speed, (SPEED_POS_X, SPEED_POS_Y)
            )

    def __on_game_over(self):
        game_rule = self.__game_rule
        is_new_best_score = game_rule.is_new_best_score
        font = gamebase.get_default_font()

        self.__update_score()
        self.__update_speed()
        prefix_best_score = (
            "NEW Best Score: " if is_new_best_score 
            else "Best Score: "
        )
        self.__text_best_score = font.render(
            prefix_best_score + str(game_rule.best_score), True, NEW_BEST_SCORE_COLOR if is_new_best_score else BEST_SCORE_COLOR
        )

        gameover_sound = None if gamesave.get("is_mute", bool) else (
            globalresources.SND_NEW_BEST_SCORE if is_new_best_score 
            else globalresources.SND_DEAD
        )
        if gameover_sound != None:
            gameover_sound.play()
    
    def __tick_game_over(self):
        screen = gamebase.get_screen()

        screen.fill(MASK_COLOR, special_flags = pygame.BLEND_RGB_MULT)
        text_gameover = self.__text_gameover
        screen.blit(
            text_gameover,
            (GAMEOVER_POS_X - text_gameover.get_width() // 2, GAMEOVER_POS_Y)
        )
        text_score = typing.cast(Surface, self.__last_text_score)
        screen.blit(
            text_score,
            (GAMEOVER_SCORE_POS_X - text_score.get_width() // 2,
             GAMEOVER_SCORE_POS_Y)
        )
        text_speed = typing.cast(Surface, self.__last_text_speed)
        screen.blit(
            text_speed, 
            (GAMEOVER_SPEED_POS_X - text_speed.get_width() // 2, 
             GAMEOVER_SPEED_POS_Y)
        )
        text_best_score = self.__text_best_score
        screen.blit(
            text_best_score,
            (GAMEOVER_BEST_SCORE_POS_X - text_best_score.get_width() // 2, 
             GAMEOVER_BEST_SCORE_POS_Y)
        )

        if self.__gameover_accept_key:
            text_key_hint = self.__text_gameover_key_hint
            screen.blit(
                text_key_hint, 
                (GAMEOVER_KEY_HINT_POS_X - text_key_hint.get_width() // 2, 
                GAMEOVER_KEY_HINT_POS_Y)
            )

        if not self.__gameover_accept_key:
            self.__gameover_accept_key_timer += float(gamebase.TICK_TIME)
            if self.__gameover_accept_key_timer >= GAMEOVER_ACCEPT_KEY_TIME:
                self.__gameover_accept_key = True
        
        if self.__gameover_accept_key:
            input_manager = self.__player_input_manager
            if input_manager.request_jump:
                gamebase.request_load_scene("GameScene")
            if input_manager.request_escape:
                gamebase.request_load_scene("MenuScene")
