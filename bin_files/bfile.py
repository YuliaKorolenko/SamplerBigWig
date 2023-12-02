import numpy as np
import time
import pandas as pd
import random
import matplotlib.pyplot as plt

PREPROCESS_FILE = "bin_files/DNA_bfile_4"
PREPROCESS_METADATA = "bin_files/bfile_metadata_4.csv"
WINDOW_SIZE = 10
LOADED_BIN = np.load(PREPROCESS_FILE)
df = pd.read_csv(PREPROCESS_METADATA)


def read_from_bin(start : int):
    return LOADED_BIN[start:(start + WINDOW_SIZE)]


def get_lines(chr : int, start : int):
    # assert start + WINDOW_SIZE  <= df.loc[chr].start + df.loc[chr].lenght, 'Make the starting position smaller or choose a different chromosome'
    return read_from_bin(df.loc[chr].start + start)


def get_time():
    global WINDOW_SIZE 
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 1000 * i

        # print(WINDOW_SIZE)
        # print(NORM_WINDOW_SIZE)
        start_time = time.time()
        for _ in range(0, 10000):
            start_pos = random.randint(0, 20000000)
            chr = random.randint(0, 2)
            ans = get_lines(0, start_pos)
        
        res_time = time.time() - start_time
        times.append(res_time)
        sizes.append(WINDOW_SIZE)
        print("--- %s seconds ---" % res_time)
    plt.xlabel('Time in seconds')
    plt.ylabel('Window size')    
    plt.plot(times, sizes,'ro')
    plt.show()

if __name__ == '__main__':    
    # get_time()
    print(get_lines(0, 0))




        
    

    
    