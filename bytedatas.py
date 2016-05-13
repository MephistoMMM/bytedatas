#!/usr/bin/env python3
"""
This file defines the class inherit from bytearray and providing some
methods to set or get data of explicit type , e.g. getUint32 or setInt8
just like buffer module in nodejs.

Now this class could provide methods to operate: 
uint8,16,32,64 , int8,16,32,64

Author: Mephis Pheies
Email: mephistommm@gmail.com
"""
from functools import wraps

class ByteDatasValueError(ValueError): 
    """for debug"""
    pass
VALID_BIT_LENGTH_OF_INT = (8, 16, 32, 64)

def parament_int(bit_len, unsigned=False):
    """
    This function return the decorator that check the bit length of them.
    The target function of decorator should has two positional paraments - 
    "seat" and "value", e.g. func(seat, value, **kargs)
    If the paraments not pass the checking, the decorator will return 
    False.
    """
    if bit_len not in VALID_BIT_LENGTH_OF_INT:
        err = "Value of bit_len should be the one of {}, but your bit_len={}."
        raise ByteDatasValueError(err.format(VALID_BIT_LENGTH_OF_INT, bit_len))

    # calculate max_value and min_value for decorator checking
    if unsigned:
        max_value = 2**bit_len - 1
        min_value = 0
    else:
        max_value = 2**(bit_len-1) - 1
        min_value = -2**(bit_len-1)

    def decorator(function):
        """decorator function"""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """check value than call function or return False directly"""
            value = args[2] if len(args) == 3 else args[1]
            if min_value <= value <= max_value:
                return function(*args, **kwargs)
            else:
                return False
        return wrapper

    return decorator


class ByteDatas(bytearray):
    """
    this class inherit from bytearray and provide some methods to set or 
    get data of explicit type.
    """

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    @parament_int(8, unsigned=True)
    def write_uint8(self, seat, value):
        """
        Set an 8-bit-length unsigned int into bytearray
        If sucess, return True.
        """
        super().__setitem__(seat, value)
        return True

    def read_uint8(self, seat):
        """
        Read an 8-bit-length unsigned int from bytearray
        """
        return super().__getitem__(seat)


