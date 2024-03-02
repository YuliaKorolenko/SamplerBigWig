import pandas as pd
import numpy as np
import os

PREPROCESS_METADATA = "bin_array/bin_metadata.csv"
df = pd.read_csv(PREPROCESS_METADATA)

def read_bw():
    print("read_bw")
    data_vector = []
    folder_path = "resfoldbigwig"

    for filename in os.listdir(folder_path):
        data_map = {}
        
        file_path = os.path.join(folder_path, filename)
        print(file_path)
        with open(file_path, "r") as file:
            for line in file:
                key, value = line.strip().split("\t")
                data_map[key] = float(value)
        
        data_vector.append(data_map)
    return data_vector

data_vector = read_bw()

def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    result_vector = []
    for cur_map in data_vector:
        ans = np.zeros(WINDOW_SIZE)
        new_start = df.loc[chr].start + start
        for i in (0, WINDOW_SIZE):
            if (new_start+i) in cur_map:
                ans[i] = cur_map[new_start+i]
        
        result_vector.append(ans)

    return result_vector

if __name__ == '__main__':
    print(get_lines(0, 0, 10))