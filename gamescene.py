'''
This module contains the content of the game scene.
'''

import typing
from blockmap import BlockMapManager
import gamebase
from player import Player, PlayerInputManager
from scene import Scene

class GameScene(Scene):
    '''
    The game scene is where the game is actually played.
    '''

    def on_create(self):
        blockmap_manager = typing.cast(
            BlockMapManager, self.spawn_entity(BlockMapManager))
        blockmap_manager.launch(lambda blockmap: None)
        self.spawn_entity(PlayerInputManager)
        self.spawn_entity(Player)

    def on_destroy(self):
        pass
