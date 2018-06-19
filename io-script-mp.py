import gaussianadd
import multiprocessing as mp
import numpy as np
import pyaudio
import queue
import struct
import time

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
FORMAT = pyaudio.paInt16


def get_input(in_frames):
    # global STOP
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    output=True,
                    frames_per_buffer=CHUNK)
    while True:
        in_frames.put(stream.read(CHUNK))


def feed(in_frames, out_frames):
    # global STOP
    while True:
        out_frames.put(gaussianadd.add_gauss(np.fromstring(in_frames.get(), np.int16), CHUNK))
        #out_frames.put(in_frames.get())


def play_out(out_frames):
    # global STOP
    p = pyaudio.PyAudio()
    stream2 = p.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=int(RATE / 2),
                     input=True,
                     output=True,
                     frames_per_buffer=CHUNK)
    while True:
        # samples = out_frames.get()
        # samp_write = struct.pack('%dh' % len(samples), *samples)
        stream2.write(out_frames.get())


if __name__ == "__main__":

    STOP = mp.Value("b", False)
    # collection queue
    in_frames = mp.Queue()
    # output queue
    out_frames = mp.Queue()

    print("* recording")

    t_1_write = mp.Process(target=get_input, args=(in_frames,))
    t_1_write.daemon = True
    t_1_write.start()

    t_2_write = mp.Process(target=feed, args=(in_frames, out_frames))
    t_2_write.daemon = True
    t_2_write.start()

    t_3_write = mp.Process(target=play_out, args=(out_frames,))
    t_3_write.daemon = True
    t_3_write.start()

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            print('* halted')
            STOP = True
            t_1_write.terminate()
            t_2_write.terminate()
            t_3_write.terminate()
            exit(0)