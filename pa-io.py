# Uses multithreading
import numpy as np
import pastream as ps
import pyaudio
import queue
import threading
import time
import ctypes
import sys

CHUNK = 1
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paFloat32


def get_input():
    global STOP
    with ps.InputStream(samplerate=RATE, channels=CHANNELS) as stream_in:
        while not STOP:
            for chunk in stream_in.chunks(chunksize=CHUNK):
                #print(type(chunk[1]))
                in_frames.put(chunk)


def feed():
    global STOP
    while not STOP:
        temp = in_frames.get()
        out_frames.put(temp)


def play_out():
    # with ps.OutputStream(samplerate=RATE, channels=CHANNELS, dtype=ctypes.c_int16) as stream_out:
    #     stream_out.set_source(out_frames)
    #     stream_out.play(out_frames)
    while not STOP:
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

    in_frames = queue.Queue()
    #out_frames = ps.RingBuffer(CHUNK*2, size=8192*4)
    out_frames = queue.Queue()

    p = pyaudio.PyAudio()

    stream2 = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     output=True,
                     frames_per_buffer=CHUNK)

    main()
