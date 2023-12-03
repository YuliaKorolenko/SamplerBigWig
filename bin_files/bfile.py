import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

PREPROCESS_FILE = "bin_files/DNA_bfile_4"
PREPROCESS_METADATA = "bin_files/bfile_metadata_4.csv"
LOADED_BIN = np.load(PREPROCESS_FILE)
df = pd.read_csv(PREPROCESS_METADATA)

def read_from_bin(start : int, WINDOW_SIZE : int):
    return LOADED_BIN[start:(start + WINDOW_SIZE)]


def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    # assert start + WINDOW_SIZE  <= df.loc[chr].start + df.loc[chr].lenght, 'Make the starting position smaller or choose a different chromosome'
    return read_from_bin(df.loc[chr].start + start, WINDOW_SIZE)

if __name__ == '__main__':    
    # get_time()
    print(get_lines(0, 0, 100))




        
    

    
    