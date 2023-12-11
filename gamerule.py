import typing
from blockmap import BlockMapManager
from blockmap_generator import BlockMapGenerator
import gamebase
from decimal import Decimal
from player import Player
from scene import DynamicEntity, SingletonEntity

class GameRule(SingletonEntity, DynamicEntity):

    __player: Player
    __blockmap_manager: BlockMapManager
    __blockmap_generator: BlockMapGenerator

    __score: Decimal = Decimal(0)
    
    __is_game_over: bool = False

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
            if self.__player.is_dead:
                self.__is_game_over = True
                self.__blockmap_manager.is_stopped = True
                self.__blockmap_generator.destroy()
                self.__blockmap_generator = None # type:ignore
        
        
