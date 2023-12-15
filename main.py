'''
The entry of the game program.
'''

import gamebase
from gamescene import GameScene
from menuscene import MenuScene

gamebase.register_scene("MenuScene", MenuScene)
gamebase.register_scene("GameScene", GameScene)
gamebase.run("MenuScene") 