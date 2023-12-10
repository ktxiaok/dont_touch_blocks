'''
This module contains the content of the game scene.
'''

import gamebase
from player import Player
from scene import Scene

class GameScene(Scene):
    '''
    The game scene is where the game is actually played.
    '''

    def on_create(self):
        self.spawn_entity(Player)

    def on_destroy(self):
        pass
