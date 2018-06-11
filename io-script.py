import pyaudio
import queue
import numpy as np
import gaussianadd
import threading
from threading import Timer
import struct
import time


CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
FORMAT = pyaudio.paInt16


def get_input(): #figure out dropping frames
    global STOP
    while not STOP:
        data = stream.read(CHUNK)
        in_frames.put(data)


def feed():
    global STOP
    while not STOP:
        out_frames.put(gaussianadd.add_gauss(np.fromstring(in_frames.get(), np.int16), CHUNK))


def play_out():
    global STOP
    while not STOP:
        samples = out_frames.get()
        #samp_write = struct.pack('%dh' % len(samples), *samples)
        stream2.write(samples)


def main():
    global STOP

    print("* recording")

    #thread to write to queue using get_input
    t_1_write = threading.Thread(target=get_input)
    t_1_write.daemon = True
    t_1_write.start()

    #thread to feed packets to gaussianadd and store in new queue
    t_2_write = threading.Thread(target=feed)
    t_2_write.daemon = True
    t_2_write.start()

    #thread to play output
    # t_3_write = threading.Thread(target=play_out)
    # t_3_write.daemon = True
    # t_3_write.start()
    t=Timer(5, play_out) #is choppy
    t.start()


    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('* halted')
            STOP = True
            exit(0)


if __name__ == "__main__":

    STOP = False
    #collection queue
    in_frames = queue.Queue()
    #output queue
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
                    rate=RATE*4,
                    output=True,
                    frames_per_buffer=CHUNK)

    main()