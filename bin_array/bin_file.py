from bitarray import bitarray
import numpy as np
import pandas as pd
import concurrent.futures

PREPROCESS_METADATA = "bin_array/bin_metadata.csv"

A_FILE = open("bin_array/A", 'rb')
C_FILE = open("bin_array/C", 'rb')
G_FILE = open("bin_array/G", 'rb')
T_FILE = open("bin_array/T", 'rb')
df = pd.read_csv(PREPROCESS_METADATA)


def function1(start : int, WINDOW_SIZE : int, FILE_CUR):
    FILE_CUR.seek(start // 8)
    el = bitarray()
    el.fromfile(FILE_CUR, WINDOW_SIZE // 8 + 1)
    numpy_ar =  np.asarray(el.tolist()[0:WINDOW_SIZE], dtype=np.uint8)
    return numpy_ar

def get_lines(chr : int, start : int, WINDOW_SIZE : int):
    new_start = df.loc[chr].start + start

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future1 = executor.submit(function1, new_start, WINDOW_SIZE, A_FILE)
        future2 = executor.submit(function1, new_start, WINDOW_SIZE, C_FILE)
        future3 = executor.submit(function1, new_start, WINDOW_SIZE, G_FILE)
        future4 = executor.submit(function1, new_start, WINDOW_SIZE, T_FILE)

        result1 = future1.result()
        result2 = future2.result()
        result3 = future3.result()
        result4 = future4.result()

    return result1, result2, result3, result4


if __name__ == '__main__':
    print(get_lines(0, 0, 100000))