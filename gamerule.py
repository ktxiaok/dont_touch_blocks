import typing
from blockmap import BlockMapManager
import gamebase
from decimal import Decimal
from player import Player
from scene import DynamicEntity, SingletonEntity

class GameRule(SingletonEntity, DynamicEntity):

    __player: Player
    __blockmap_manager: BlockMapManager

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

    def on_tick(self):
        dt = gamebase.TICK_TIME

        if not self.__is_game_over:
            self.__score += dt
            if self.__player.is_dead:
                self.__is_game_over = True
                self.__blockmap_manager.is_stopped = True
        
        
