# Uses multithreading
import gaussianadd
import multiprocessing as mp
import numpy as np
import pyaudio
import queue
import struct
import threading
import time


CHUNK = 1024
CHANNELS = 2
RATE = 44100
FORMAT = pyaudio.paInt16

#we want two ring buffers, 1 for frames, 1 for history OR 1 large list
#one pointer writes, and second one manages the get
#when the two differ by some distance in the frame buffer, we reset the get pointer to the writing pointer
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
