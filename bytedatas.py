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
    This function return the decorator that change paraments to valid vlaue 
    and check the bit length of them.
    The target function of decorator should has two positional paraments - 
    "seat" and "value", e.g. func(seat, value, **kargs)
    If the paraments not pass the checking, the decorator will return 
    False.
    """
    if bit_len not in VALID_BIT_LENGTH_OF_INT:
        err = "Value of bit_len should be the one of {}, but your bit_len={}."
        raise ByteDatasValueError(err.format(VALID_BIT_LENGTH_OF_INT, bit_len))

    # calculate type_max_value for changing raw value to valid value
    type_max_value = 2**bit_len
    # calculate the region of value
    if unsigned is True:
        max_value = 2**bit_len
        min_value = 0
    else:
        max_value = 2**(bit_len-1)
        min_value = -2**(bit_len-1)

    def decorator(function):
        """decorator function"""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """
            change valid to positive if value < 0
            check value than call function or return False directly
            """
            args = list(args)
            value, index = (args[2], 2) if len(args) == 3 else (args[1], 1)

            if min_value <= value < max_value:
                # The reason changing negative value to positive is that it's
                # easy while getting every bytes from value.
                value = type_max_value + value if value < 0 else value
                args[index] = value
                return function(*args, **kwargs)
            else:
                return False
        return wrapper

    return decorator


def return_int(bit_len, unsigned=False):
    """
    This function return the decorator that change return value to valid value.
    The target function of decorator should return only one value
    e.g. func(*args, **kargs) -> value:
    """
    if bit_len not in VALID_BIT_LENGTH_OF_INT:
        err = "Value of bit_len should be the one of {}, but your bit_len={}."
        raise ByteDatasValueError(err.format(VALID_BIT_LENGTH_OF_INT, bit_len))

    # calculate max_value for changing raw value to valid value
    max_value = 2**bit_len

    def decorator(function):
        """decorator function"""
        @wraps(function)
        def wrapper(*args, **kwargs):
            """
            change valid to positive if value < 0
            check value than call function or return False directly
            """
            value = function(*args, **kwargs)
            
            if value >= max_value or value < 0:
                err = ("Returned value of {} should be between 0 and {}, but your "
                       "value = {}.")
                raise ByteDatasValueError(err.format(function.__name__, max_value, value))

            if unsigned is False:
                # if value > max_value//2 , it means the top bit of value is
                # 1 , it is a negative value, so we should change it to negative
                value = value - max_value if value > max_value//2 else value
            return value
        return wrapper

    return decorator

class ByteDatas(bytearray):
    """
    this class inherit from bytearray and provide some methods to set or 
    get data of explicit type.
    """

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        setattr(self, "write_uint{}".format(8), 
                self.__create_write_int_method(8, True))
        setattr(self, "write_int{}".format(8),
                self.__create_write_int_method(8))

    def __create_write_int_method(self, bit_len, unsigned=False):
        """
        This function will create write method for any int type.
        Without this function , you may should write 8 methods totally for 
        int types.
        """
        byte_len = bit_len // 8
        def write_method(seat, value):
            """
            Write an int, whose signed depends on variate 'unsigned' and
            length of bits depends on variate 'bit_len', into bytedatas.
            If sucess, return True.
            """
            for i in range(byte_len):
                super(ByteDatas, self).__setitem__(seat+i, value & 0xFF)
                value >>= 8
            return True

        # call parament_int function to generate an appropriate decorator 
        # for method
        return parament_int(bit_len, unsigned=unsigned)(write_method)

    # @parament_int(8, unsigned=True)
    # def write_uint8(self, seat, value):
        # """
        # Write an 8-bit-length unsigned int into bytearray
        # If sucess, return True.
        # """
        # super().__setitem__(seat, value)
        # return True

    @return_int(8, unsigned=True)
    def read_uint8(self, seat):
        """
        Read an 8-bit-length unsigned int from bytearray
        """
        return super().__getitem__(seat)

    # @parament_int(8)
    # def write_int8(self, seat, value):
        # """
        # Write an 8-bit-length int into bytearray
        # If sucess, return True.
        # """
        # super().__setitem__(seat, value)
        # return True

    @return_int(8)
    def read_int8(self, seat):
        """
        Read an 8-bit-length int from bytearray
        """
        return super().__getitem__(seat)


