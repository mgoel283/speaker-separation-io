# Uses multithreading
import numpy as np
import pyaudio
from pastream import RingBuffer
import queue
import threading
import time

CHUNK = 64
CHANNELS = 1
RATE = 16000
FORMAT = pyaudio.paInt16
HIST_SECS = 2


def get_input():
    global STOP
    while not STOP:
        temp = stream_in.read(CHUNK, exception_on_overflow=False)
        in_frames.write(temp)


def feed(): #do history stuff here
    global STOP
    while not STOP:
        out_frames.put(hist_read()[0])


def play_out():
    global STOP
    while not STOP:
        # samples = out_frames.get()
        temp = out_frames.get()
        stream_out.write(temp)


def hist_read():
    back_amount = int(HIST_SECS*RATE/CHUNK)
    in_frames.advance_read_index(-back_amount)

    history_data = in_frames.read(back_amount)
    print(history_data)

    return in_frames.read(), history_data


def main():
    global STOP

    print("* recording")

    # thread to write to queue using get_input
    t_1_write = threading.Thread(target=get_input)
    t_1_write.daemon = True
    t_1_write.start()

    # thread to feed packets to API and store in new queue
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
    in_frames = RingBuffer(CHUNK * 2, size=32768)
    out_frames = queue.Queue()

    p = pyaudio.PyAudio()

    stream_in = p.open(format=FORMAT,
                       channels=CHANNELS,
                       rate=RATE,
                       input=True,
                       frames_per_buffer=CHUNK)

    stream_out = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

    main()
