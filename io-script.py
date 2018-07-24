# Uses multithreading
import gaussianadd
import numpy as np
import pyaudio
import queue
import threading
import multiprocessing as mp
import time
import matplotlib.pyplot as plt
import ringbuffer

CHUNK = 1
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paInt16
#fill_val = b'\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'


# when the two differ by some distance in the frame buffer, we reset the get pointer to the writing pointer
# and essentially drop the preceding frames
# class RingBuffer:
#     def __init__(self, size_max, out_size):
#         self.write_head = 0  # index of pointer to write
#         self.get_front = 0  # index of front of frame data
#         self.get_back = -10  # index of back of frame data
#         self.max = size_max
#         self.data = []
#
#     class __Full:
#         def put(self, x):
#             self.data[self.write_head] = x
#             self.write_head = (self.write_head + 1) % self.max
#
#         def get(self):
#             if self.get_front > self.get_back:
#                 history = b''.join(self.data[self.get_back: self.get_front])
#                 #return self.data[self.get_front], history
#                 return self.data[self.get_front]
#             else:
#                 history = b''.join(self.data[self.get_back:] + self.data[:self.get_front])
#                 #return self.data[self.get_front], history
#                 return self.data[self.get_front]
#
#
#     def put(self, x):
#         self.data.append(x)
#         if len(self.data) == self.max:
#             self.__class__ = self.__Full
#
#     def get(self):
#         try:
#             if self.get_front > self.get_back:
#                 history = b''.join(self.data[self.get_back: self.get_front])
#                 #return self.data[self.get_front], history
#                 return self.data[self.get_front]
#             else:
#                 history = b''.join(self.data[self.get_back:] + self.data[:self.get_front])
#                 #return self.data[self.get_front], history
#                 return self.data[self.get_front]
#             self.get_front = (self.get_front + 1) % self.max
#             self.get_back = (self.get_back + 1) % self.max
#         except Exception as e:
#             return b'\x00\x00\x00\x00\xff\xff\x00\x00'


def get_input():
    global STOP
    while not STOP:
        in_frames.put(stream.read(CHUNK, exception_on_overflow=False))


def feed():
    global STOP
    while not STOP:
        #temp = in_frames.get()
        #out_frames.put(gaussianadd.add_reverb(np.fromstring(in_frames.get(), np.int8)))
        temp = in_frames.get()
        print(temp)
        out_frames.put(temp)


def play_out():
    global STOP
    while not STOP:
        # samples = out_frames.get()
        stream2.write(out_frames.get())


def main():
    global STOP

    print("* recording")

    # thread to write to queue using get_input
    t_1_write = threading.Thread(target=get_input)
    t_1_write.daemon = True
    t_1_write.start()

    # thread to feed packets to gaussianadd and store in new queue
    t_2_write = threading.Thread(target=feed)
    t_2_write.daemon = True
    t_2_write.start()

    # thread to play output
    t_3_write = threading.Thread(target=play_out)
    t_3_write.daemon = True
    t_3_write.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('* halted')
            STOP = True
            exit(0)


if __name__ == "__main__":
    STOP = False
    in_frames = ringbuffer.RingBuffer(8192, dtype=bytes)
    #in_frames = queue.Queue()
    # output queue
    out_frames = queue.Queue()

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)

    stream2 = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     output=True,
                     frames_per_buffer=CHUNK)

    main()
