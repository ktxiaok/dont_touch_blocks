'''
This module provides some useful tools.
'''

from decimal import Decimal
from typing import Any, NoReturn, Sequence, Tuple, Union, Self

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

    @staticmethod 
    def raise_operand_error(obj: Any) -> NoReturn:
        raise ValueError("invalid operand: " + str(obj))
    
class InvalidOperationException(Exception):
    pass