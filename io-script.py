"""
I/O script to pass chunks(frames) of audio data and history
Plays processed audio back
"""
import numpy as np
import pyaudio
from pastream import RingBuffer
import queue
import threading
import time

CHUNK = 64
CHANNELS = 2
RATE = 16000
FORMAT = pyaudio.paInt16
HIST_SECS = 2


def get_input():
    """
    Writes incoming audio data to in_frames (pastream RingBuffer object)
    """
    global STOP
    while not STOP:
        in_frames.write(stream_in.read(CHUNK, exception_on_overflow=False))


def feed():
    """
    Takes data from in_frames and gives it to some module for processing
    Puts processed frame into out_frames (queue)
    """
    global STOP
    while not STOP:
        out_frames.put(hist_read()[0])  # this line will feed data to API


def play_out():
    """
    Plays audio on PyAudio stream
    """
    global STOP
    while not STOP:
        stream_out.write(out_frames.get())


def hist_read():
    """
    :return: tuple with (current chunk, past N seconds of history)
    """
    back_amount = int(HIST_SECS*RATE/CHUNK)

    in_frames.advance_read_index(-back_amount)
    history_data = in_frames.read(back_amount)

    return in_frames.read(), history_data


def main():
    """
    Starts and manages threads
    """
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


def closest_two(num):
    """
    :return: Integer that is the closest power of 2 to num rounded up
    """
    exp = np.ceil(np.log2(num))
    return int(np.power(2, exp))


if __name__ == "__main__":
    STOP = False

    # holds ~5 times the history data
    in_frames = RingBuffer(CHUNK * 2, size=closest_two(int(5*HIST_SECS*RATE/CHUNK)))
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
