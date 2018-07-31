# import numpy as np
# import threading as th
# import multiprocessing as mp
# import ctypes
# import collections
#
#
# class RingBuffer:
    # def __init__(self, size_max, dtype=bytes):
    #     self.write_head = 0  # index of pointer to write
    #     self.get_front = -1  # index of front of frame data
    #     self.max = size_max
    #     self.data = np.empty(size_max, dtype=dtype)
    #
    # def put(self, x):
    #     self.data[self.write_head] = x
    #     self.write_head = (self.write_head + 1) % self.max
    #
    # def get(self):
    #     self.get_front = (self.get_front + 1) % self.max
    #     return self.data[self.get_front]

    # def __init__(self, max_size, dtype=np.float32):
    #     self._npa = mp.RawArray(ctypes.c_char_p, max_size * 2)
    #     self.max_size = max_size
    #     self._index = 0
    #     self.read_head = -1
    #
    # def put(self, element):
    #
    #     self._npa[self._index % self.max_size] = element
    #     self._npa[(self._index % self.max_size) + self.max_size] = element
    #     self._index += 1
    #
    # def get(self):
    #     if self.read_head >= self._index:
    #         self.read_head = self._index - 1
    #     self.read_head = (self.read_head + 1) % self.max_size
    #     return self._npa[self.read_head]

    # def __init__(self, max_size):
    #     self._data = collections.deque(maxlen=max_size)
    #
    # def put(self, element):
    #     self._data.appendleft(element)
    #
    # def get(self):
    #     self._data.pop()


# if __name__ == "__main__":
#     test_buff = RingBuffer(4)
#     test_buff.put(5)
#     test_buff.put(6)
#     test_buff.put(7)
#     test_buff.put(8)
#     test_buff.put(9)
#     print(test_buff[:3])
