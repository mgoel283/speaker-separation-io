#adds gaussian noise to input segment
#simulates Yi's program
import numpy as np


def add_gauss(chunk, chunk_size):
    #noise = np.random.normal(0, 1, chunk_size*2)
    #return chunk + .01*noise
    return chunk + .01*np.ones(chunk_size*2)