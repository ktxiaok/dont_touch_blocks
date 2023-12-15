'''
The entry of the game program.
'''

import gamebase
from gamescene import GameScene

gamebase.register_scene("GameScene", GameScene)
gamebase.run("GameScene") 