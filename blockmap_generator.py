from decimal import Decimal
import decimal
from threading import Thread
import threading
import time
from typing import List, Tuple
import typing
import gamebase
from scene import DynamicEntity, SingletonEntity
import player
import blockmap
from blockmap import Block, BlockMap, BlockMapManager
import random

from utils import DecimalVector2

PLAYER_POS_Y_MIN = 60
PLAYER_POS_Y_MAX = gamebase.WINDOW_DIMENSION[1] - 60
PLAYER_POS_Y_JUMPABLE_MIN = PLAYER_POS_Y_MIN + player.PLAYER_JUMP_HEIGHT + 1
PLAYER_JUMP_INTERVAL_MIN = 0.2
PLAYER_JUMP_INTERVAL_MAX = (
        2 * (PLAYER_POS_Y_MAX - PLAYER_POS_Y_MIN) / 
        float(gamebase.GRAVITY_ACCEL)
    ) ** 0.5

PLAYER_PATH_Y_OFFSET_RANGE_START = DecimalVector2(Decimal(1), Decimal(5))
PLAYER_PATH_Y_OFFSET_RANGE_END = DecimalVector2(Decimal(0), Decimal(2))
PLAYER_PATH_Y_OFFSET_TO_END_TIME = Decimal(120)
PLAYER_PATH_Y_OFFSET_CHANGE_SPEED = (
    PLAYER_PATH_Y_OFFSET_RANGE_END - PLAYER_PATH_Y_OFFSET_RANGE_START
) / PLAYER_PATH_Y_OFFSET_TO_END_TIME

class BlockMapGenerator(SingletonEntity, DynamicEntity):
    __blockmap_manager: BlockMapManager

    __blockmap_speed: Decimal = player.PLAYER_INITIAL_SPEED

    __player_speed_x: Decimal = player.PLAYER_INITIAL_SPEED
    __player_speed_y: Decimal = Decimal(0)
    __player_pos_y: Decimal
    __player_offset_x: Decimal = Decimal(0)
    
    __player_path: List[Tuple[int, int]] # the index means the block position x and the element means (min_y, max_y)
    __player_path_y_offset_range: DecimalVector2 = PLAYER_PATH_Y_OFFSET_RANGE_START
    __player_path_y_offset_range_is_changing: bool = True

    __work_thread: Thread
    __thread_stop_flag: bool = False

    def on_spawn(self):
        super().on_spawn()
        self.__blockmap_manager = typing.cast(
            BlockMapManager, self.scene.get_singleton_entity(BlockMapManager)
        )
        self.__player_pos_y = Decimal(
            random.uniform(
                PLAYER_POS_Y_MIN, PLAYER_POS_Y_MAX
            )
        )
        self.__player_path = [None] * blockmap.BLOCK_MAP_WIDTH # type:ignore
        self.__blockmap_manager.launch(
            lambda initial_bmap: self.__generate(initial_bmap)
        )
        self.__work_thread = Thread(target = self.__run_work_thread)
        self.__work_thread.start()

    def on_destroy(self):
        super().on_destroy()
        self.__thread_stop_flag = True

    def on_tick(self):
        dt = gamebase.TICK_TIME

        if self.__blockmap_speed < player.PLAYER_MAX_SPEED:
            self.__blockmap_speed += player.PLAYER_SPEED_ACCEL * dt
            if self.__blockmap_speed > player.PLAYER_MAX_SPEED:
                self.__blockmap_speed = player.PLAYER_MAX_SPEED
        self.__blockmap_manager.move(self.__blockmap_speed * dt)

        if self.__player_path_y_offset_range_is_changing:
            self.__player_path_y_offset_range += typing.cast(DecimalVector2, PLAYER_PATH_Y_OFFSET_CHANGE_SPEED * dt)
            if self.__player_path_y_offset_range.x <= PLAYER_PATH_Y_OFFSET_RANGE_END.x:
                self.__player_path_y_offset_range = PLAYER_PATH_Y_OFFSET_RANGE_END
                self.__player_path_y_offset_range_is_changing = False

    
    def __run_work_thread(self):
        blockmap_manager = self.__blockmap_manager
        while True:
            if self.__thread_stop_flag:
                break
            bmap = blockmap_manager.try_get_unready_blockmap()
            if bmap == None:
                continue
            self.__generate(bmap)
            blockmap_manager.put_ready_blockmap(bmap)
            time.sleep(0.001)
            

    def __generate(self, bmap: BlockMap):
        bpos_x = 0
        dt = gamebase.TICK_TIME
        bpos_y_min: int = None # type:ignore
        bpos_y_max: int = None # type:ignore
        jump_timer = self.__get_next_jump_time()
        while True:
            if self.__player_offset_x >= blockmap.BLOCK_SIDE_LEN:
                self.__player_offset_x -= blockmap.BLOCK_SIDE_LEN
                self.__player_path[bpos_x] = (bpos_y_min, bpos_y_max)
                bpos_x += 1
                if bpos_x >= blockmap.BLOCK_MAP_WIDTH:
                    break
                bpos_y_min = None # type:ignore
                bpos_y_max = None # type:ignore
            player_bpos_y = int(self.__player_pos_y / blockmap.BLOCK_SIDE_LEN)
            if bpos_y_min == None or player_bpos_y < bpos_y_min:
                bpos_y_min = player_bpos_y
            if bpos_y_max == None or player_bpos_y > bpos_y_max:
                bpos_y_max = player_bpos_y
            if jump_timer <= 0:
                jump_timer = self.__get_next_jump_time()
                if self.__player_pos_y > PLAYER_POS_Y_JUMPABLE_MIN:
                    self.__player_speed_y = -player.PLAYER_JUMP_SPEED
            elif self.__player_pos_y >= PLAYER_POS_Y_MAX:
                jump_timer = self.__get_next_jump_time()
                self.__player_speed_y = -player.PLAYER_JUMP_SPEED
            jump_timer -= dt
            self.__player_speed_y += gamebase.GRAVITY_ACCEL * dt
            self.__player_pos_y += self.__player_speed_y * dt
            if self.__player_speed_x < player.PLAYER_MAX_SPEED:
                self.__player_speed_x += player.PLAYER_SPEED_ACCEL * dt
                if self.__player_speed_x > player.PLAYER_MAX_SPEED:
                    self.__player_speed_x = player.PLAYER_MAX_SPEED
            self.__player_offset_x += self.__player_speed_x * dt
        for x in range(blockmap.BLOCK_MAP_WIDTH):
            player_y_min, player_y_max = self.__player_path[x]
            player_y_min -= self.__get_player_path_y_offset()
            player_y_max += self.__get_player_path_y_offset()
            if player_y_min > 0:
                y_min_exc = player_y_min
                color = (
                    random.randint(0, 128), 
                    random.randint(0, 128), 
                    random.randint(0, 128) 
                )
                for y in reversed(range(y_min_exc)):
                    bmap.set_block(x, y, Block(color))
                    color = tuple(
                        max(comp - random.randint(0, 50), 0) for comp in color
                    )
            if player_y_max < blockmap.BLOCK_MAP_HEIGHT - 1:
                y_max = player_y_max + 1
                color = (
                    random.randint(0, 128), 
                    random.randint(0, 128), 
                    random.randint(0, 128) 
                )
                for y in range(y_max, blockmap.BLOCK_MAP_HEIGHT):
                    bmap.set_block(x, y, Block(color))
                    color = tuple(
                        max(comp - random.randint(0, 50), 0) for comp in color
                    )
        bmap.refresh()

    def __get_next_jump_time(self) -> Decimal:
        SHORT_RANGE = (PLAYER_JUMP_INTERVAL_MIN, 0.5)
        LONG_RANGE = (0.5, PLAYER_JUMP_INTERVAL_MAX)
        SHORT_RANGE_PROB = 0.8
        r = SHORT_RANGE if random.random() <= SHORT_RANGE_PROB else LONG_RANGE
        return Decimal(random.uniform(r[0], r[1]))
    
    def __get_player_path_y_offset(self) -> int:
        offset_range = self.__player_path_y_offset_range
        return int(
            Decimal(
                random.uniform(float(offset_range.x), float(offset_range.y))
            ).quantize(Decimal(1), rounding = decimal.ROUND_HALF_EVEN)
        )
            
            
            
        
