import numpy as np
import pandas as pd
import os

# positions = np.load('bin_search_big_wig/positions.npy')
# values_ziped = np.load('bin_search_big_wig/values_ziped.npy')
# pos_size = len(positions)

PREPROCESS_METADATA = "bin_array/bin_metadata.csv"
df = pd.read_csv(PREPROCESS_METADATA)
output_path = "bnbigwig"

def preprocess_all_data(folder_path):
    all_positions = []
    all_values_ziped = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith("_data_positions.npy"):
            positions = np.load(os.path.join(folder_path, filename))
            values_ziped = np.load(os.path.join(folder_path, filename.replace("_positions.npy", "_values.npy")))
            all_positions.append(positions)
            all_values_ziped.append(values_ziped)
    
    return all_positions, all_values_ziped

# Preprocess all numpy arrays
all_positions, all_values_ziped = preprocess_all_data(output_path)

def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    ans_all = []
    
    for positions, values_ziped in zip(all_positions, all_values_ziped):
        ans = np.zeros(WINDOW_SIZE)
        new_start = df.loc[chr].start + start

        j = bin_search(positions, new_start)
        while j < len(positions) and (positions[j] - new_start) < WINDOW_SIZE:
            ans[positions[j] - new_start] = values_ziped[j]
            j += 1

        ans_all.append(ans)
    
    return ans_all

# def get_lines(chr : int, start : int, WINDOW_SIZE : int):
#     ans = np.zeros(WINDOW_SIZE)
#     new_start = df.loc[chr].start + start
    
#     j = bin_search(new_start)
#     while (j < pos_size and (positions[j] - new_start) < WINDOW_SIZE):
#         ans[positions[j] - new_start] = values_ziped[j]
#         j += 1

#     return ans

def bin_search(positions, cur):
    l = -1
    r = len(positions)
    while (r - l > 1):
        m = (l + r) // 2
        if (positions[m] < cur):
            l = m
        else:
            r = m

    return r

if __name__ == '__main__':
    # 23   3976130   100000
    print(get_lines(2, 180749, 10))