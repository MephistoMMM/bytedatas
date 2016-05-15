#!/usr/bin/env python3
"""
This is a test file for bytedatas package

Author: Mephis Pheies
Email: mephistommm@gmail.com
"""
from bytedatas.bytedatas import ByteDatas

TEST_BYTEDATAS_LEN = 100

def test_bytedatas():
    """
    test bytedatas
    * write_uint8 and read_uint8
    * write_int8 and read_int8
    """
    bds = ByteDatas(TEST_BYTEDATAS_LEN)

    # uint8
    bds[2] = 124
    index_2 = bds.read_uint8(2)
    assert index_2 == 124

    # sucess to write
    assert bds.write_uint8(3, 100) is True
    assert bds.read_uint8(3) == 100

    # failed to write
    assert bds.write_uint8(40, 258) is False
    assert bds.read_uint8(40) == 0

    # int8
    bds[5] = 124
    index_5 = bds.read_int8(5)
    assert index_5 == 124
    bds[6] = 256-124
    index_6 = bds.read_int8(6)
    assert index_6 == -124

    # success to write
    assert bds.write_int8(7, 100) is True
    assert bds.read_int8(7) == 100
    assert bds.write_int8(8, -100) is True
    assert bds.read_int8(8) == -100

    # failed to write
    assert bds.write_int8(9, -230) is False
    assert bds.write_int8(10, 230) is False

    # success to write
    assert bds.write_int32(19, 3241) is True
    assert bds.read_int32(19) == 3241
    assert bds.write_int32(23, -3241) is True
    assert bds.read_int32(23) == -3241

    # failed to write
    assert bds.write_int32(27, -2**31-100) is False
    assert bds.write_int32(31, 2**31+100) is False

    # bytes 
    series_bytes = b"bytes"
    assert bds.write_series_bytes(60, series_bytes, 8) is True
    assert bds.read_series_bytes(60, 8).rstrip(b"\x00") == series_bytes
    assert bds.write_series_bytes(90, "it is failed", 9) is False


