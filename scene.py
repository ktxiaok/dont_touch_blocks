'''
This module is mainly about scenes and entities.
'''

import typing
from typing import List, Set, Dict, Type, Optional
from abc import ABC, abstractmethod
import pygame
from utils import DecimalVector2, InvalidOperationException

class Scene(ABC):
    '''
    Represent for a stage of the game, a collection or manager of game entities.

    This class is responsible for managing a group of associated game entities, 
    including spawning entities, updating entities, distributing events to entities, and so on. Concrete scenes should be implemented by inheriting this class.
    '''

    __entities: Set["Entity"]
    __dynamic_entities: List["DynamicEntity"]
    __pygame_event_listener_entities: List["PygameEventListenerEntity"]
    __singleton_entities: Dict[Type["SingletonEntity"], "SingletonEntity"]
    
    def __init__(self):
        self.__entities = set()
        self.__dynamic_entities = []
        self.__pygame_event_listener_entities = []
        self.__singleton_entities = {}
    
    @abstractmethod
    def on_create(self):
        '''
        This method will be called when the scene is initializing.
        '''

        pass

    @abstractmethod
    def on_destroy(self):
        '''
        This method will be called when the scene is being destroyed.
        '''

        pass

    def spawn_entity(self, entity_type: Type["Entity"]):
        '''
        Spawn a entity in the scene.

        Args:
            entity_type: A type of the entity to spawn, which must be the subclass of Entity.

        Returns:
            A spawned entity instance.

        Raises:
            TypeError: The argument type is not correct.
            ValueError: Arg entity_type is not the subclass of Entity.
        '''

        if not isinstance(entity_type, type):
            raise TypeError("Arg entity_type must be a type!")
        if not issubclass(entity_type, Entity):
            raise ValueError("Arg entity_type must be the subclass of Entity!")
        
        entity = entity_type(self)
        self.__entities.add(entity)
        if isinstance(entity, DynamicEntity):
            self.__dynamic_entities.append(entity)
        if isinstance(entity, PygameEventListenerEntity):
            self.__pygame_event_listener_entities.append(entity)
        if isinstance(entity, SingletonEntity):
            if entity_type in self.__singleton_entities:
                raise InvalidOperationException(f"Couldn't spawn the singleton entity of the type {entity_type}: there's alreay a instance!")
            self.__singleton_entities[typing.cast(Type[SingletonEntity], entity_type)] = entity
            
        entity.on_spawn()

        return entity
    
    def get_singleton_entity(self, entity_type: Type["SingletonEntity"]) -> Optional["SingletonEntity"]:
        return self.__singleton_entities.get(entity_type)
    
    def _remove_entity(self, entity: "Entity"):
        '''
        Remove the entity instance from the game scene.

        This method can only be called by Entity.destroy!
        '''

        self.__entities.remove(entity)
        if isinstance(entity, DynamicEntity):
            self.__dynamic_entities.remove(entity)
        if isinstance(entity, PygameEventListenerEntity):
            self.__pygame_event_listener_entities.remove(entity)
        if isinstance(entity, SingletonEntity):
            del self.__singleton_entities[type(entity)]
    
    def _tick(self):
        '''
        Update the game scene, i.e. step forward a game frame.

        This method can only be called by the module gamebase!
        '''

        entity_buffer = self.__dynamic_entities.copy()
        for entity in entity_buffer:
            entity.on_tick()
        for entity in entity_buffer:
            entity.on_late_tick()

    def _destroy(self):
        '''
        Destroy the scene.

        This method can only be called by the module gamebase!
        '''

        entity_buffer: List[Entity] = []
        for entity in self.__entities:
            entity_buffer.append(entity)
        for entity in entity_buffer:
            entity.destroy()
        self.on_destroy()
    
    def _send_pygame_event(self, event: pygame.event.Event):
        '''
        Send the pygame event instance to all entities of class PygameEventListenerEntity.

        This method can only be called by the module gamebase!
        '''

        entity_buffer = self.__pygame_event_listener_entities.copy()
        for entity in entity_buffer:
            entity.on_pygame_event(event)

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

    def on_late_tick(self):
        '''
        This method will be called after the method on_tick of all entities is called
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