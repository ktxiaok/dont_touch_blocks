from abc import ABC, abstractmethod
from decimal import Decimal
from utils import DecimalVector2
from scene import Scene

class Entity(ABC):
    '''
    This is an abstract class representing for the game entity.

    A game entity is an individual having special function in the game scene. 
    '''

    __scene: Scene = None
    
    __is_destroyed: bool = False

    def __init__(self, scene: Scene):
        '''
        This constructor can only be called by the class Scene!
        '''

        self.__scene = scene

    @property
    def scene(self):
        '''
        Returns the Scene instance this entity belongs to.
        '''

        return self.__scene
    
    @property
    def is_destroyed(self):
        '''
        Returns whether the entity instance has been destroyed. 
        '''
        
        return self.__is_destroyed
    
    def on_spawn(self):
        '''
        When a new entity instance is spawned, this method will be called.
        '''

        pass

    def on_destroy(self):
        '''
        This method will be called when the entity instance is to be destroyed.
        '''

        pass

    def destroy(self):
        '''
        Destroy the entity instance.
        '''

        if self.__is_destroyed:
            return
        
        self.on_destroy()
        self.__is_destroyed = True
        self.__scene._remove_entity(self)

class SingletonEntity(Entity):
    pass

class PygameEventListenerEntity(Entity):
    @abstractmethod
    def on_pygame_event(self, event):
        pass

class DynamicEntity(Entity):
    def on_tick(self):
        pass

class PositionalEntity(Entity):
    __pos = DecimalVector2()
    
    @property
    def pos(self):
        return self.__pos
    
    @pos.setter
    def pos(self, pos):
        self.__pos = pos