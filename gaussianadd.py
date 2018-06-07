#adds gaussian noise to input segment (mechanics tbd)
#simulates Yi's program
import numpy as np


def add_gauss(chunk, chunk_size):
    noise = np.random.normal(0, 1, chunk_size*2)
    #return str(np.dot(chunk, noise))
    return str(noise)

