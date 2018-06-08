#adds gaussian noise to input segment
#simulates Yi's program
import numpy as np


def add_gauss(chunk, chunk_size):
    noise = np.random.normal(0, 1000, chunk_size*2)
    return np.add(chunk, noise)
    #return chunk