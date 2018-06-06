#trying to write to thread safe queue
import pyaudio
import queue

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 1
FORMAT = pyaudio.paInt16


def main():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    frames = queue.Queue()

    try:
        while True:
            data = stream.read(CHUNK)
            frames.put(data)
    except KeyboardInterrupt:
        print('halted')
        print(frames.get())

    print(frames.get()) #for testing


if __name__ == "__main__":
    main()

