#script to test gaussianadd
#outputs a plot and two wave files
import pyaudio
import queue
import wave
import numpy as np
import matplotlib.pyplot as plt
import gaussianadd

CHUNK = 1024
WIDTH = 2
CHANNELS = 2
RATE = 1600
FORMAT = pyaudio.paInt16


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
        exp_new = np.exp(-3 * np.linspace(1, RATE * 2, num=RATE * 2) / RATE)
        h = np.random.random(size=RATE * 2) * exp_new
        # while not frames.empty():
        #     output_frames.put(gaussianadd.add_gauss(frames.get(), CHUNK))
        for i in range(0, len(frames)):
            gauss_chunk = gaussianadd.add_reverb(np.fromstring(frames[i], np.int8), h)
            output_frames.append(gauss_chunk)
        #Printing waveform for testing
        fig = plt.figure()
        s = fig.add_subplot(211)
        amp = np.fromstring(frames_temp, np.int8) #ndarray
        s.plot(amp)
        s2 = fig.add_subplot(212)
        s2.plot(output_frames)
        plt.show()

        stream.stop_stream()
        stream.close()
        p.terminate()

        #WAV conversion code
        wf = wave.open('original.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        wf = wave.open('output.wav', 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE*4)
        wf.writeframes(b''.join(output_frames))
        wf.close()


if __name__ == "__main__":
    main()