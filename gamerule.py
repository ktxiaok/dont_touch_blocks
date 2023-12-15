import typing
from blockmap import BlockMapManager
from blockmap_generator import BlockMapGenerator
import gamebase
from decimal import Decimal
from player import Player
from scene import DynamicEntity, SingletonEntity
import gamesave

class GameRule(SingletonEntity, DynamicEntity):
    '''
    This class is responsible for implementing the game rule, such as determining whether the game is over, calculating the score, etc.
    '''

    __player: Player
    __blockmap_manager: BlockMapManager
    __blockmap_generator: BlockMapGenerator

    __score: Decimal = Decimal(0)
    __player_speed: Decimal = Decimal(0)
    
    __is_game_over: bool = False

    __is_new_best_score: bool = False
    __best_score: Decimal = Decimal(0)

    @property
    def is_game_over(self) -> bool:
        
        return self.__is_game_over

    @property
    def score(self) -> Decimal:
        
        return self.__score
    
    @property
    def player_speed(self) -> Decimal:
        
        return self.__player_speed
    
    @property
    def is_new_best_score(self) -> bool:

        return self.__is_new_best_score
    
    @property
    def best_score(self) -> Decimal:
        
        return self.__best_score

    def on_spawn(self):
        super().on_spawn()
        self.__player = typing.cast(
            Player, self.scene.get_singleton_entity(Player)
            )
        self.__blockmap_manager = typing.cast(
            BlockMapManager, self.scene.get_singleton_entity(BlockMapManager)
        )
        self.__blockmap_generator = typing.cast(
            BlockMapGenerator, self.scene.get_singleton_entity(
                BlockMapGenerator
            )
        )

    def on_tick(self):
        dt = gamebase.TICK_TIME

        if not self.__is_game_over:
            self.__score += dt
            self.__player_speed = self.__blockmap_generator.player_speed
            if self.__player.is_dead:
                self.__is_game_over = True
                self.__blockmap_manager.is_stopped = True
                self.__blockmap_generator.destroy()
                self.__blockmap_generator = None # type:ignore
                score = self.score.quantize(Decimal("1.0"))
                best_score = gamesave.get_best_score()
                if score > best_score:
                    self.__is_new_best_score = True
                    best_score = score
                    gamesave.set_best_score(best_score)
                self.__best_score = best_score
        
        
