# 000 - T
# 001 - C
# 010 - A
# 011 - G
# 100 - N
import numpy as np
from dataclasses import dataclass
import math
import time
import pandas as pd
import random
import matplotlib.pyplot as plt

PREPROCESS_FILE = "less_memory/DNA"
PREPROCESS_METADATA = "less_memory/metadata.csv"
BYTE_SIZE = 8
WINDOW_SIZE = 100
NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)
df = pd.read_csv(PREPROCESS_METADATA)


def get_lines(chr : int, start : int):
    assert start + WINDOW_SIZE  <= (df.loc[chr].byte_count * 8 - df.loc[chr].waste_bits) // 3 , 'Make the starting position smaller or choose a different chromosome'
    return bits_to_one_hot(df.loc[chr].start + math.ceil(start * 3 / BYTE_SIZE), start * 3 % BYTE_SIZE) 


def bits_to_one_hot(start, start_in_byte):
    file = open(PREPROCESS_FILE, 'rb') 
    file.seek(start)
    bits = file.read(NORM_WINDOW_SIZE)

    j = 0
    G = [0] * WINDOW_SIZE
    T = [0] * WINDOW_SIZE
    A = [0] * WINDOW_SIZE
    C = [0] * WINDOW_SIZE

    j = 0
    odds_and_ends = bin(bits[0])[2:].zfill(8)[start_in_byte:]
    for i in range(1, len(bits)):
        byte = bits[i]
        binary = bin(byte) 
        new_string = odds_and_ends + binary[2:].zfill(8)
        for k in range(0, len(new_string), 3):
            i = new_string[k:k+3]
            if (i == '011'):
                G[j] = 1
            elif (i == '001'):
                T[j] = 1
            elif (i == '100'):
                A[j] = 1
            elif (i == '010'):
                C[j] = 1
            j += 1
            if j == WINDOW_SIZE - 1:
                return G, T, A, C
        ost = len(new_string)%3
        odds_and_ends = new_string[:-ost]

    return G, T, A, C

def get_time():
    global WINDOW_SIZE 
    global NORM_WINDOW_SIZE
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 1000 * i
        NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)
        print("WINDOW SIZE", WINDOW_SIZE)
        start_time = time.time()
        for _ in range(0, 10000):
            chr = random.randint(0, 4)
            start_pos = random.randint(0, 20000000)
            G, T, A, C = get_lines(chr, start_pos)
        
        res_time = time.time() - start_time
        times.append(res_time)
        sizes.append(WINDOW_SIZE)
        print("--- %s seconds ---" % res_time)
    plt.xlabel('Time in seconds')
    plt.ylabel('Window size')    
    plt.plot(times, sizes,'ro')
    plt.show()

if __name__ == '__main__':
    get_time()
    # G, T, A, C = get_lines(0, 0)
    # print(G)
    # print(T)
    # print(A)
    # print(C)