#trying to write to thread safe queue
import pyaudio
import queue
#import wave
import numpy
import matplotlib.pyplot as plt

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
#RECORD_SECONDS = 1
FORMAT = pyaudio.paInt16
WAVE_OUTPUT_FILENAME = "output.wav"



def main():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    #frames = queue.Queue()
    frames = []
    try:
        while True:
            data = stream.read(CHUNK)
            #frames.put(data)
            frames.append(data)
    except KeyboardInterrupt:
        frames = b''.join(frames)
        print('halted')
        fig = plt.figure()
        s = fig.add_subplot(111)
        amp = numpy.fromstring(frames, numpy.int16)
        s.plot(amp)
        plt.show()
        #print(numpy.fromstring(frames.get(), numpy.dtype('Int16')))
        #WAV conversion code
        # stream.stop_stream()
        # stream.close()
        # p.terminate()
        #
        # wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        # wf.setnchannels(CHANNELS)
        # wf.setsampwidth(p.get_sample_size(FORMAT))
        # wf.setframerate(RATE)
        # wf.writeframes(b''.join(frames))
        # wf.close()


if __name__ == "__main__":
    main()

