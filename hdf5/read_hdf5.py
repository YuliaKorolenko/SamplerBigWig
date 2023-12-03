import numpy as np
import time
import pandas as pd
import random
import matplotlib.pyplot as plt
import h5py

PREPROCESS_FILE = "hdf5/DNA_hdf5_4"
PREPROCESS_METADATA = "hdf5/hdf5_metadata_4.csv"
LOADED_HDF5 = h5py.File(PREPROCESS_FILE, 'r')
A = LOADED_HDF5['A']
C = LOADED_HDF5['C']
G = LOADED_HDF5['G']
T = LOADED_HDF5['T']
df = pd.read_csv(PREPROCESS_METADATA)

def read_from_bin(start : int, WINDOW_SIZE : int):
    end = start + WINDOW_SIZE
    return A[start:end], C[start:end], G[start:end], T[start:end]

def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    # assert start + WINDOW_SIZE  <= df.loc[chr].start + df.loc[chr].lenght, 'Make the starting position smaller or choose a different chromosome'
    return read_from_bin(df.loc[chr].start + start, WINDOW_SIZE)

if __name__ == '__main__':    
    print(get_lines(0, 0, 30))