import pandas as pd
import numpy as np

PREPROCESS_METADATA = "bin_array/bin_metadata.csv"
df = pd.read_csv(PREPROCESS_METADATA)

def read_bw():
    data_map = {}
    
    with open("big_wig_hash_map/data_map.txt", "r") as file:
        for line in file:
            key, value = line.strip().split("\t")
            data_map[key] = float(value)
    
    return data_map

data_map = read_bw()

def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    ans = np.zeros(WINDOW_SIZE)
    new_start = df.loc[chr].start + start
    for i in (0, WINDOW_SIZE):
        if (new_start+i) in data_map:
            print(new_start)
            ans[i] = data_map[new_start+i]
    
    return ans

if __name__ == '__main__':
    print(get_lines(0, 0, 10))
