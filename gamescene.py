'''
This module contains the content of the game scene.
'''

import typing
from basicscene import BasicScene
from blockmap import BlockMapManager
from blockmap_generator import BlockMapGenerator
import gamebase
from gamerule import GameRule
from gameui import GameUi
from player import Player, PlayerInputManager
from scene import Scene

class GameScene(BasicScene):
    '''
    The game scene is where the game is actually played.
    '''

    def on_create(self):

        super().on_create()
        self.spawn_entity(BlockMapManager)
        self.spawn_entity(BlockMapGenerator)
        self.spawn_entity(Player)
        self.spawn_entity(GameRule)
        self.spawn_entity(GameUi)
