# 000 - T
# 001 - C
# 010 - A
# 011 - G
# 100 - N
from dataclasses import dataclass
import math
import pandas as pd

PREPROCESS_FILE = "less_memory/DNA"
PREPROCESS_METADATA = "less_memory/metadata.csv"
BYTE_SIZE = 8
df = pd.read_csv(PREPROCESS_METADATA)


def read_bits_from_file(filepath, start, start_in_byte):
    file =  open(filepath, 'rb')
    file.seek(start)
    byte_array = file.read(NORM_WINDOW_SIZE)
    int_list = list(byte_array)
    
    bits_list = [format(byte, '08b') for byte in int_list]
    
    bits_string = ''.join(bits_list)[start_in_byte:start_in_byte + (WINDOW_SIZE * 3)]
    return bits_string


def get_lines(chr : int, start : int, WINDOW_SIZE_ : int):
    global WINDOW_SIZE 
    global NORM_WINDOW_SIZE
    WINDOW_SIZE = WINDOW_SIZE_
    NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)
    assert start + WINDOW_SIZE  <= (df.loc[chr].byte_count * 8 - df.loc[chr].waste_bits) // 3 , 'Make the starting position smaller or choose a different chromosome'
    bits_string = read_bits_from_file(PREPROCESS_FILE, df.loc[chr].start + math.ceil(start * 3 / BYTE_SIZE), start * 3 % BYTE_SIZE)
    return bits_to_one_hot(bits_string)


def bits_to_one_hot(bits_string):
    j = 0
    G = [0] * WINDOW_SIZE
    T = [0] * WINDOW_SIZE
    A = [0] * WINDOW_SIZE
    C = [0] * WINDOW_SIZE
    for k in range(0, len(bits_string), 3):
        i = bits_string[k:k+3]
        if (i == '011'):
            G[j] = 1
        elif (i == '001'):
            T[j] = 1
        elif (i == '100'):
            A[j] = 1
        elif (i == '010'):
            C[j] = 1
        j += 1
    return G, T, A, C

if __name__ == '__main__':
    G, T, A, C = get_lines(0, 10000, 30)
    # 18 12435040 30
    # 3 10850248 30
    # 0 10000 30
    print(G)
    print(T)
    print(A)
    print(C)
    print(len(C))




        
    

    
    