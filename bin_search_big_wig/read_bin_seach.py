import numpy as np
import pandas as pd

positions = np.load('bin_search_big_wig/positions.npy')
values_ziped = np.load('bin_search_big_wig/values_ziped.npy')
pos_size = len(positions)

PREPROCESS_METADATA = "bin_array/bin_metadata.csv"
df = pd.read_csv(PREPROCESS_METADATA)

def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    ans = np.zeros(WINDOW_SIZE)
    new_start = df.loc[chr].start + start
    
    j = bin_search(new_start)
    while (j < pos_size and (positions[j] - new_start) < WINDOW_SIZE):
        ans[positions[j] - new_start] = values_ziped[j]
        j += 1

    return ans

def bin_search(cur):
    l = -1
    r =pos_size
    while (r - l > 1):
        m = (l + r) // 2
        if (positions[m] < cur):
            l = m
        else:
            r = m

    return r

if __name__ == '__main__':
    # 23   3976130   100000
    print(get_lines(29, 180749, 100))