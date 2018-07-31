# adds gaussian noise to input segment
# simulates Yi's program
# import numpy as np
# import matplotlib.pyplot as plt
#
#
# def add_gauss(chunk, chunk_size):
#     try:
#         noise = np.random.normal(0, 1, chunk_size*4)
#         # check for 2 second data
#         # if #someCheck:
#         #     # print('Received 2s data')
#         #return np.add(chunk, noise)
#         return chunk
#     except Exception as e:
#         print('Not yet')
#
#
# def add_reverb(chunk):
#     # chunk_fft = np.fft.fft(chunk)
#     # #result = chunk_fft * h_fft
#     # return np.fft.ifft(chunk_fft)
#     #return np.convolve(chunk, h)
#     return chunk

import sys
from numbers import Number
from collections import Set, Mapping, deque

try:  # Python 2
    zero_depth_bases = (basestring, Number, xrange, bytearray)
    iteritems = 'iteritems'
except NameError:  # Python 3
    zero_depth_bases = (str, bytes, Number, range, bytearray)
    iteritems = 'items'


def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, zero_depth_bases):
            pass  # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, iteritems):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, iteritems)())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size

    return inner(obj_0)