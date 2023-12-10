from abc import ABC, abstractmethod
from decimal import Decimal
from utils import DecimalVector2
from scene import Scene
import pygame

class Entity(ABC):
    '''
    This is an abstract class representing for the game entity.

    A game entity is an individual having special function in the game scene. 
    '''

    __scene: Scene
    
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
    '''
    No more than one instance of this type is allowed in a scene.

    Instances of this type can be accessed by Scene.get_singleton_entity. 
    '''

    pass

class PygameEventListenerEntity(Entity):
    '''
    Represents for a event listener entity for pygame events.
    '''

    @abstractmethod
    def on_pygame_event(self, event: pygame.event.Event):
        '''
        This method will be called when a pygame event occurs.

        Args:
            event: A pygame.event.Event instance that occurs.
        '''

        pass

class DynamicEntity(Entity):
    '''
    Entities of this type will be updated on every game tick(in other word, frame).
    '''

    def on_tick(self):
        '''
        This method will be called on every game tick.
        '''

        pass

class PositionalEntity(Entity):
    '''
    Represents for entities that have a 2d decimal position.
    '''
    
    __pos: DecimalVector2 = DecimalVector2()
    
    @property
    def pos(self):
        return self.__pos
    
    @pos.setter
    def pos(self, pos):
        self.__pos = pos