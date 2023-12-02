import numpy as np
import time
import pandas as pd
import random
import matplotlib.pyplot as plt
import h5py

PREPROCESS_FILE = "hdf5/DNA_hdf5"
PREPROCESS_METADATA = "hdf5/hdf5_metadata.csv"
WINDOW_SIZE = 10
LOADED_HDF5 = h5py.File(PREPROCESS_FILE, 'r')
A = LOADED_HDF5['A']
C = LOADED_HDF5['C']
G = LOADED_HDF5['G']
T = LOADED_HDF5['T']
df = pd.read_csv(PREPROCESS_METADATA)


def read_from_bin(start : int):
    end = start + WINDOW_SIZE
    return A[start:end], C[start:end], G[start:end], T[start:end]


def get_lines(chr : int, start : int):
    # assert start + WINDOW_SIZE  <= df.loc[chr].start + df.loc[chr].lenght, 'Make the starting position smaller or choose a different chromosome'
    return read_from_bin(df.loc[chr].start + start)


def get_time():
    global WINDOW_SIZE 
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 100000 * i

        print(WINDOW_SIZE)
        # print(NORM_WINDOW_SIZE)
        start_time = time.time()
        for _ in range(0, 1000):
            start_pos = random.randint(0, 20000000)
            chr = random.randint(0, 20)
            ans = get_lines(0, start_pos)
        
        res_time = time.time() - start_time
        times.append(res_time)
        sizes.append(WINDOW_SIZE)
        print("--- %s seconds ---" % res_time)
    plt.ylabel('Time in seconds')
    plt.xlabel('Window size')    
    plt.plot(sizes, times, 'ro')
    plt.show()

if __name__ == '__main__':    
    get_time()
    # print(get_lines(0, 0))