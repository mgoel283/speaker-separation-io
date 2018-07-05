# adds gaussian noise to input segment
# simulates Yi's program
import numpy as np
import matplotlib.pyplot as plt


def add_gauss(chunk, chunk_size):
    try:
        noise = np.random.normal(0, 1, chunk_size*4)
        # check for 2 second data
        # if #someCheck:
        #     # print('Received 2s data')
        #return np.add(chunk, noise)
        return chunk
    except Exception as e:
        print('Not yet')


def add_reverb(chunk, h):
    #try_this = np.fft.fft(chunk)
    return chunk
    #return np.convolve(chunk, h)
