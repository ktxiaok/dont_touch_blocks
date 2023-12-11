'''
This module is mainly about a data structure 'block map'.
'''

from queue import Queue
from typing import Callable, List, Optional, Tuple
import pygame
from pygame import Rect, draw
from pygame import Color, Surface
import gamebase
from scene import DynamicEntity, SingletonEntity
from utils import ColorValue
from decimal import Decimal

BLOCK_SIDE_LEN = 40

class Block:
    '''
    A data structure representing a square block that the player can't touch.
    '''

    color: Color

    def __init__(self, color_value: ColorValue):
        self.color = Color(color_value)

BLOCK_MAP_SURFACE_WIDTH = gamebase.WINDOW_DIMENSION[0]
BLOCK_MAP_SURFACE_HEIGHT = gamebase.WINDOW_DIMENSION[1]
BLOCK_MAP_WIDTH = BLOCK_MAP_SURFACE_WIDTH // BLOCK_SIDE_LEN
BLOCK_MAP_HEIGHT = BLOCK_MAP_SURFACE_HEIGHT // BLOCK_SIDE_LEN
BLOCK_MAP_SIZE = BLOCK_MAP_WIDTH * BLOCK_MAP_HEIGHT

class BlockMap:
    '''
    A data structure representing a two-dimensional block map.

    This map contains an list of Optional[Block](None represent no block) and a corresponding pygame.Surface instance. The surface is the same size as the game window.
    '''

    __blocks: List[Optional[Block]]
    __surface: Surface
    __offset_x: Decimal = Decimal(BLOCK_MAP_SURFACE_WIDTH)

    def __init__(self, is_first: bool = False):
        if is_first:
            self.__offset_x = Decimal(0)
        self.__blocks = [None] * BLOCK_MAP_SIZE
        self.__surface = Surface(
            (BLOCK_MAP_SURFACE_WIDTH, BLOCK_MAP_SURFACE_HEIGHT), flags = pygame.SRCALPHA)
        
    @property
    def surface(self) -> Surface:
        '''
        Returns the corresponding Surface instance.
        '''

        return self.__surface
    
    @property
    def offset_x(self) -> Decimal:
        '''
        Returns the offset as a world position X.
        '''

        return self.__offset_x
    
    @property
    def is_invalid(self) -> bool:
        '''
        Returns whether this block map is out of the game window.

        Calling method recycle can make it usable again.
        '''

        return self.__offset_x <= -BLOCK_MAP_SURFACE_WIDTH
        
    def get_block(self, x: int, y: int) -> Optional[Block]:
        '''
        Returns the block at the specified block position.

        Args:
            x: Block position X.
            y: Block position Y.

        Raises:
            IndexError: The specified position is out of the range.
        '''

        return self.__blocks[x * BLOCK_MAP_HEIGHT + y]
    
    def set_block(self, x: int, y: int, block: Optional[Block]):
        '''
        Set the block at the specified block position.

        Args:
            x: Block position X.
            y: Block position Y.
            block: The Block instance to set.

        Raises:
            IndexError: The specified position is out of the range.
        '''

        self.__blocks[x * BLOCK_MAP_HEIGHT + y] = block

    def pos_world_to_block(self, x: Decimal, y: Decimal) -> Tuple[int, int]:
        '''
        Convert a world position to a block position.

        Args:
            x: World position X.
            y: World position Y.
        
        Returns:
            The corresponding block position as a tuple.
        '''

        origin_x = self.__offset_x
        block_x = int((x - origin_x) / BLOCK_SIDE_LEN)
        block_y = int(y / BLOCK_SIDE_LEN)
        return (block_x, block_y)

    def refresh(self):
        '''
        Refresh the Surface instance according to the block map.
        '''

        self.__surface.fill((0, 0, 0, 0))
        for x in range(BLOCK_MAP_WIDTH):
            for y in range(BLOCK_MAP_HEIGHT):
                block = self.get_block(x, y)
                if block != None:
                    draw.rect(
                        self.__surface, block.color, 
                        Rect(
                            x * BLOCK_SIDE_LEN, y * BLOCK_SIDE_LEN, BLOCK_SIDE_LEN, BLOCK_SIDE_LEN
                        )
                    )

    def move(self, dx: Decimal):
        '''
        Move the block map.

        Args:
            dx: The world distance to move on the X-axis. 
        '''

        self.__offset_x -= dx

    @offset_x.setter
    def offset_x(self, x: Decimal):
        '''
        Set the world offset x directly to avoid precision issue.

        Args:
            x: The world position x to set.
        '''

        self.__offset_x = x

    def recycle(self):
        '''
        Reset the block map and make it usable again.
        '''

        for i in range(BLOCK_MAP_SIZE):
            self.__blocks[i] = None
        self.__offset_x = Decimal(BLOCK_MAP_SURFACE_WIDTH)

READY_BLOCK_MAP_MAX_COUNT = 3

class BlockMapManager(SingletonEntity, DynamicEntity):
    '''
    A manager of all block maps in a game scene.
    '''
    
    __blockmap1: BlockMap
    __blockmap2: BlockMap
    __ready_blockmaps: Queue[BlockMap]
    __unready_blockmaps: Queue[BlockMap]

    __is_stopped: bool = False

    @property
    def is_stopped(self):
        return self.__is_stopped
    
    @is_stopped.setter
    def is_stopped(self, stopped: bool):
        self.__is_stopped = stopped

    def launch(self, init_callback: Callable[[BlockMap], None]):
        self.__blockmap1 = BlockMap(is_first = True)
        self.__blockmap2 = BlockMap()
        self.__ready_blockmaps = Queue()
        self.__unready_blockmaps = Queue()
        init_callback(self.__blockmap2)

    def __test_touch_block_for_blockmap(self, bmap: BlockMap, x: Decimal, y: Decimal) -> bool:
        bpos_x, bpos_y = bmap.pos_world_to_block(x, y)
        if bpos_x < 0 or bpos_x >= BLOCK_MAP_WIDTH:
            return False
        if bpos_y < 0 or bpos_y >= BLOCK_MAP_HEIGHT:
            return False
        block = bmap.get_block(bpos_x, bpos_y)
        return block != None

    def test_touch_block(self, x: Decimal, y: Decimal) -> bool:
        if self.__test_touch_block_for_blockmap(self.__blockmap1, x, y):
            return True
        if self.__test_touch_block_for_blockmap(self.__blockmap2, x, y):
            return True
        return False

    def on_tick(self):
        dt = gamebase.TICK_TIME
        if self.__blockmap1.is_invalid:
            unready_blockmap = self.__blockmap1
            unready_blockmap.recycle()
            self.__unready_blockmaps.put(unready_blockmap)
            self.__blockmap1 = self.__blockmap2
            self.__blockmap2 = self.__ready_blockmaps.get()
        blockmap_count_need = READY_BLOCK_MAP_MAX_COUNT - self.__ready_blockmaps.qsize()
        if blockmap_count_need > 0:
            unready_blockmap_count_need = blockmap_count_need - self.__unready_blockmaps.qsize()
            if unready_blockmap_count_need > 0:
                for i in range(unready_blockmap_count_need):
                    self.__unready_blockmaps.put(BlockMap())
        
        
        screen = gamebase.get_screen()
        screen.blit(
            self.__blockmap1.surface, (int(self.__blockmap1.offset_x), 0)
        )
        screen.blit(
            self.__blockmap2.surface, (int(self.__blockmap2.offset_x), 0)
        )
        
    def move(self, dx: Decimal):
        self.__blockmap1.move(dx)
        self.__blockmap2.offset_x = self.__blockmap1.offset_x + BLOCK_MAP_SURFACE_WIDTH

    def try_get_unready_blockmap(self) -> Optional[BlockMap]:
        try:
            return self.__unready_blockmaps.get_nowait()
        except:
            return None
    
    def put_ready_blockmap(self, blockmap: BlockMap):
        self.__ready_blockmaps.put(blockmap)
    