import typing
from typing import List, Set, Dict, Type, Optional
from abc import ABC, abstractmethod
from entity import Entity, DynamicEntity, PygameEventListenerEntity, SingletonEntity
import pygame
from gamebase import InvalidOperationException

class Scene(ABC):
    '''
    Represent for a stage of the game, a collection or manager of game entities.

    This class is responsible for managing a group of associated game entities, 
    including spawning entities, updating entities, distributing events to entities, and so on. Concrete scenes should be implemented by inheriting this class.
    '''

    __entities: Set[Entity]
    __dynamic_entities: List[DynamicEntity]
    __pygame_event_listener_entities: List[PygameEventListenerEntity]
    __singleton_entities: Dict[Type[SingletonEntity], SingletonEntity]
    
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

    def spawn_entity(self, entity_type: Type[Entity]):
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
    
    def get_singleton_entity(self, entity_type: Type[SingletonEntity]) -> Optional[SingletonEntity]:
        return self.__singleton_entities.get(entity_type)
    
    def _remove_entity(self, entity: Entity):
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
    
    def _send_pygame_event(self, event: pygame.event.Event):
        '''
        Send the pygame event instance to all entities of class PygameEventListenerEntity.

        This method can only be called by the module gamebase!
        '''

        entity_buffer = self.__pygame_event_listener_entities.copy()
        for entity in entity_buffer:
            entity.on_pygame_event(event)