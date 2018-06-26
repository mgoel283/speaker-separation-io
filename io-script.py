# Uses multithreading
import gaussianadd
#import scikits.audiolab as audiolab
import numpy as np
import pyaudio
import queue
import threading
import time

CHUNK = 1024
CHANNELS = 2
RATE = 44100
FORMAT = pyaudio.paInt16


# when the two differ by some distance in the frame buffer, we reset the get pointer to the writing pointer
# and essentially drop the preceding frames
class RingBuffer:
    def __init__(self, size_max, out_size):
        self.write_head = 0  # index of pointer to write
        self.get_front = out_size  # index of front of frame data
        self.get_back = 0  # index of back of frame data
        self.max = size_max
        self.data = []

    class __Full:
        def put(self, x):
            self.data[self.write_head] = x
            self.write_head = (self.write_head + 1) % self.max

        def get(self):
            if self.get_front > self.get_back:
                history = b''.join(self.data[self.get_back: self.get_front])
                return self.data[self.get_front], history
            else:
                history = b''.join(self.data[self.get_back:] + self.data[:self.get_front])
                return self.data[self.get_front], history
            self.get_front = (self.get_front + 1) % self.max
            self.get_back = (self.get_back + 1) % self.max

    def put(self, x):
        self.data.append(x)
        if len(self.data) == self.max:
            self.__class__ = self.__Full

    def get(self):
        try:
            if self.get_front > self.get_back:
                history = b''.join(self.data[self.get_back: self.get_front])
                return self.data[self.get_front], history
            else:
                history = b''.join(self.data[self.get_back:] + self.data[:self.get_front])
                return self.data[self.get_front], history
            self.get_front = (self.get_front + 1) % self.max
            self.get_back = (self.get_back + 1) % self.max
        except Exception as e:
            return b'\x00\x00\x00\x00\xff\xff\x00\x00', b'\x00\x00\x00\x00\xff\xff\x00\x00'


def get_input():
    global STOP
    while not STOP:
        in_frames.put(stream.read(CHUNK))


def feed():
    global STOP
    while not STOP:
        out_frames.put(gaussianadd.add_gauss(np.fromstring(in_frames.get(), np.int8), CHUNK))
        # out_frames.put(in_frames.get())


def play_out():
    global STOP
    while not STOP:
        # samples = out_frames.get()
        # samp_write = struct.pack('%dh' % len(samples), *samples)
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
    # collection queue
    #in_frames = RingBuffer(500, 2)
    in_frames = queue.Queue()
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
