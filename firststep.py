#trying to write to thread safe queue
import pyaudio
import queue
import wave
import numpy
import matplotlib.pyplot as plt
import gaussianadd


CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 44100
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
            data = stream.read(CHUNK) #each data point is a bytes object
            #frames.put(data)
            frames.append(data)
    except KeyboardInterrupt:
        frames_temp = b''.join(frames) #bytes
        # print('halted')
        output_frames = []
        # while not frames.empty():
        #     output_frames.put(gaussianadd.add_gauss(frames.get(), CHUNK))
        for i in range(0, len(frames)):
            gauss_chunk = gaussianadd.add_gauss(numpy.fromstring(frames[i], numpy.int16), CHUNK)
            output_frames.append(gauss_chunk)
        #Printing waveform for testing
        fig = plt.figure()
        s = fig.add_subplot(211)
        amp = numpy.fromstring(frames_temp, numpy.int16) #ndarray
        s.plot(amp)
        s2 = fig.add_subplot(212)
        s2.plot(output_frames)
        plt.show()

        #WAV conversion code
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open('original.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE*4)
        wf.writeframes(b''.join(output_frames))
        wf.close()


if __name__ == "__main__":
    main()