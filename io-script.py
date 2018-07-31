# Uses multithreading
import numpy as np
import pyaudio
import queue
import threading
import time
from pastream import RingBuffer

CHUNK = 64
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paInt16


def get_input():
    global STOP
    while not STOP:
        in_frames.write(stream.read(CHUNK, exception_on_overflow=False))


def feed():
    global STOP
    while not STOP:
        try:
            out_frames.put(in_frames.read())
        except IndexError:
            print('yeet')


def play_out():
    global STOP
    while not STOP:
        # samples = out_frames.get()
        temp = out_frames.get()
        stream2.write(temp)


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
    in_frames = RingBuffer(CHUNK*2, size=8192*4)
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
