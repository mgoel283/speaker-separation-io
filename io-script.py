import pyaudio
import queue
import numpy
import matplotlib.pyplot as plt
import gaussianadd
import threading


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
        #give gaussianadd a frame
        #write output frame to queue

def play_out():
    global STOP
    while not STOP:
        #play audio from output queue

def main():
    global STOP
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    #thread to write to queue using get_input
    t_1_write = threading.Thread(target = get_input())
    t_1_write.daemon = True

    #thread to feed packets to gaussianadd and store in new queue
    t_2_write = threading.Thread(target=feed())
    t_2_write.daemon = True

    #thread to play output
    t_3_write = threading.Thread(target=play_out())
    t_3_write.daemon = True

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

    main()