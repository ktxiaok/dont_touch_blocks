'''
This module provides some useful tools.
'''

from decimal import Decimal
from typing import Any, NoReturn, Sequence, Tuple, Union, Self
import typing
from enum import IntEnum
from pygame import Color

Numeric = Union[int, float, str, Decimal]
ColorValue = Union[Color, str, Sequence[int]]
 
def try_decimal(num: Any) -> Any:
    '''
    Try to convert the arg num to a Decimal object.

    Args:
        num: A numeric object trying to be converted to a Decimal object.

    Returns:
        A corresponding Decimal object will be returned if the type of arg num is int, float, or str. Otherwise arg num itself will be returned.
    '''

    if isinstance(num, Decimal):
        return num
    elif isinstance(num, int) or isinstance(num, float) or isinstance(num, str):
        return Decimal(num)
    else:
        return num

class DecimalVector2:
    '''
    Represents for a mathematical two-dimensional vector based on Decimal. 
    '''

    x: Decimal
    y: Decimal

    def __init__(self, x: Numeric = Decimal(0), y: Numeric = Decimal(0)):
        x = try_decimal(x)
        y = try_decimal(y)
        if not (isinstance(x, Decimal) and isinstance(y, Decimal)):
            raise ValueError("invalid arguments: " + "(" + str(x) + "," + str(y) + ")")
        self.x = x
        self.y = y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, DecimalVector2):
            return False
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other: Self) -> Self:
        if isinstance(other, DecimalVector2):
            return DecimalVector2(self.x + other.x, self.y + other.y)
        else:
            self.raise_operand_error(other)
    
    def __sub__(self, other: Self) -> Self:
        if isinstance(other, DecimalVector2):
            return DecimalVector2(self.x - other.x, self.y - other.y)
        else:
            self.raise_operand_error(other)

    # if 'other' is a vector, it will do a dot product.
    def __mul__(self, other: Union[Self, Numeric]) -> Union[Decimal, Self]:
        other = try_decimal(other)
        if isinstance(other, DecimalVector2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Decimal):
            return DecimalVector2(other * self.x, other * self.y)
        else:
            self.raise_operand_error(other)

    def __truediv__(self, other: Numeric) -> Self:
        other = try_decimal(other)
        if isinstance(other, Decimal):
            return DecimalVector2(self.x / other, self.y / other)
        else:
            self.raise_operand_error(other)

    def __iadd__(self, other: Self) -> Self:
        return self + other

    def __isub__(self, other: Self) -> Self:
        return self - other

    def __imul__(self, other: Numeric) -> Self:
        return typing.cast(DecimalVector2, self * other)

    def __idiv__(self, other: Numeric) -> Self:
        return self / other

    @staticmethod 
    def raise_operand_error(obj: Any) -> NoReturn:
        raise ValueError("invalid operand: " + str(obj))
    
class InvalidOperationException(Exception):
    pass

class FadeState(IntEnum):
    IN = 0
    HOLD = 1
    OUT = 2

class FadeEffect:

    __time_tuple: tuple[float, float, float]

    __state: int = int(FadeState.IN)
    __timer: float = 0.0
    __is_finished: bool = False
    
    def __init__(self, in_time: float, hold_time: float, out_time: float):
        self.__time_tuple = (in_time, hold_time, out_time)
    
    @property
    def is_finished(self) -> bool:
        return self.__is_finished
    
    @property
    def value(self) -> float:
        if self.__is_finished:
            return 0.0
        state = self.__state
        if state == FadeState.IN:
            return self.__timer / self.__time_tuple[state]
        if state == FadeState.HOLD:
            return 1.0
        return 1 - self.__timer / self.__time_tuple[state]
    
    def update(self, delta_time: float):
        self.__timer += delta_time
        while True:
            state = self.__state
            limit_time = self.__time_tuple[state]
            if self.__timer >= limit_time:
                if state == FadeState.OUT:
                    self.__is_finished = True
                    break
                self.__timer -= limit_time
                self.__state += 1
                continue
            break
             

