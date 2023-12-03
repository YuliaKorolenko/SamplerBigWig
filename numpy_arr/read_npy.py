import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import time

T = np.load('numpy_arr/T.npy')
A = np.load('numpy_arr/A.npy')
C = np.load('numpy_arr/C.npy')
G = np.load('numpy_arr/G.npy')
df = pd.read_csv("less_memory/metadata.csv")

def get_lines_npy(chr : int, start : int, WINDOW_SIZE : int):
    start_ = df.loc[chr].start + start
    end_ = start_ + WINDOW_SIZE
    return A[start_:end_], T[start_:end_], C[start_:end_], G[start_:end_]

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   print(get_lines_npy(0, 0, 2))