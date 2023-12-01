# some useful utils

from decimal import Decimal

# Try to convert the argument 'num' to a Decimal instance. If it failed, return 'num' itself. 
def try_decimal(num):
    if isinstance(num, Decimal):
        return num
    elif isinstance(num, int) or isinstance(num, float) or isinstance(num, str):
        return Decimal(num)
    else:
        return num

# 2d vector based on Decimal
class DecimalVector2:
    x = None
    y = None

    def __init__(self, x = Decimal(0), y = Decimal(0)):
        x = try_decimal(x)
        y = try_decimal(y)
        if not (isinstance(x, Decimal) and isinstance(y, Decimal)):
            raise ValueError("invalid arguments: " + "(" + str(x) + "," + str(y) + ")")
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, DecimalVector2):
            return False
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        if isinstance(other, DecimalVector2):
            return DecimalVector2(self.x + other.x, self.y + other.y)
        else:
            self.raise_operand_error(other)
    
    def __sub__(self, other):
        if isinstance(other, DecimalVector2):
            return DecimalVector2(self.x - other.x, self.y - other.y)
        else:
            self.raise_operand_error(other)

    # if 'other' is a vector, it will do a dot product.
    def __mul__(self, other):
        other = try_decimal(other)
        if isinstance(other, DecimalVector2):
            return self.x * other.x + self.y * other.y
        elif isinstance(other, Decimal):
            return DecimalVector2(other * self.x, other * self.y)
        else:
            self.raise_operand_error(other)

    def __truediv__(self, other):
        other = try_decimal(other)
        if isinstance(other, Decimal):
            return DecimalVector2(self.x / other, self.y / other)
        else:
            self.raise_operand_error(other)

    @staticmethod 
    def raise_operand_error(obj):
        raise ValueError("invalid operand: " + str(obj))