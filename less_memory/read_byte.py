import math
import pandas as pd
import random
import matplotlib.pyplot as plt
import time

PREPROCESS_METADATA = "less_memory/metadata.csv"
PREPROCESS_FILE = "less_memory/DNA"
WINDOW_SIZE = 10
BYTE_SIZE = 8
NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)
df = pd.read_csv(PREPROCESS_METADATA)

class Count:
    def __init__(self, start=0, start_in_byte=0):
        file = open(PREPROCESS_FILE, 'rb') 
        file.seek(start)
        self.bytes = file.read(NORM_WINDOW_SIZE + math.ceil(start_in_byte / 3))
        self.byte_num = 0
        if (len(self.bytes) > 0):
            self.byte = self.bytes[0]
            self.byte_num += 1
        self.cur_pos_in_byte = start_in_byte
        self.bit_mapping = {
            0 : 128,
            1 : 64,
            2 : 32,
            3 : 16,
            4 : 8,
            5 : 4,
            6 : 2,
            7 : 1,
        }

    def get_one_hot(self, b_1, b_2, b_3):
    # 'T': '001',
    # 'C': '010',
    # 'G': '011',
    # 'A': '100',
    # 'N': '000'
    # return C T G A
        if not b_1 and not b_2 and b_3:
            return 0, 1, 0, 0
        elif not b_1 and b_2 and b_3:
            return 0, 0, 1, 0
        elif not b_1 and b_2 and not b_3:
            return 1, 0, 0, 0
        elif b_1:
            return 0, 0, 0, 1
        else:
            return 0, 0, 0, 0
        
    def get_next_pos(self):
        if self.cur_pos_in_byte >= BYTE_SIZE and self.byte_num < len(self.bytes):
            self.byte = self.bytes[self.byte_num]
            self.byte_num += 1
            self.cur_pos_in_byte = 0
        
        self.cur_pos_in_byte += 1
        return self.cur_pos_in_byte - 1
 
    def __iter__(self):
        return self
    
    def __next__(self):
        first_bit = self.byte & self.bit_mapping[self.get_next_pos()] != 0
        second_bit = self.byte & self.bit_mapping[self.get_next_pos()] != 0
        third_bit = self.byte & self.bit_mapping[self.get_next_pos()] != 0

        return self.get_one_hot(first_bit, second_bit, third_bit)
    

def get_lines(chr : int, start : int):
    assert start + WINDOW_SIZE  <= (df.loc[chr].byte_count * 8 - df.loc[chr].waste_bits) // 3 , 'Make the starting position smaller or choose a different chromosome'
    return bits_to_one_hot(df.loc[chr].start + math.ceil(start * 3 / BYTE_SIZE), start * 3 % BYTE_SIZE) 
    
def bits_to_one_hot(start, start_in_byte):
    G = [0] * WINDOW_SIZE
    T = [0] * WINDOW_SIZE
    A = [0] * WINDOW_SIZE
    C = [0] * WINDOW_SIZE
    count_A = Count(start, start_in_byte)
    for i in range(0, WINDOW_SIZE):
        res = next(count_A)
        C[i] = res[0]
        T[i] = res[1]
        G[i] = res[2]
        A[i] = res[3]

    return G, T, A, C

def get_time():
    global WINDOW_SIZE 
    global NORM_WINDOW_SIZE
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 1000 * i
        NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)
        print(WINDOW_SIZE)
        # print(NORM_WINDOW_SIZE)
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
    # ctypes
    # WINDOW SIZE 10
    # chr  0
    # start pos  882445
    # get_lines(0, 882445)
    get_time()

    # for i in range(0, 8):
    #     print(1 << 7 - i)



        
    

    
    