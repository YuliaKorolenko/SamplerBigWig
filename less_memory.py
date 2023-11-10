# 000 - T
# 001 - C
# 010 - A
# 011 - G
# 100 - N
import struct
import numpy as np
from dataclasses import dataclass
import math
import time
import pandas as pd
from tqdm import tqdm
import random
import matplotlib.pyplot as plt

# WINDOW_SIZE = 10
PREPROCESS_FILE = "DNA"
PREPROCESS_METADATA = "metadata.csv"
BYTE_SIZE = 8
df = pd.read_csv(PREPROCESS_METADATA)
# NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)

@dataclass
class Chromosome_Info:
    number: int
    start_pos: int
    lenght: int
    wit_sep_lenght : int
    row_length : int
    with_sep_row_length : int

# Словарь для сопоставления символов с битовым представлением
bit_mapping = {
    'T': '001',
    'C': '010',
    'G': '011',
    'A': '100',
    'N': '000'
}

def convert_string_to_bits(input_string):
    bits = []
    i = 0
    for char in input_string:
        if (char != '\n'):
            bits.append(bit_mapping[char])
        i += 1
    
    bits_string = ''.join(bits)
    waste_bits = len(bits_string) % BYTE_SIZE
    if (len(bits_string) % BYTE_SIZE != 0):
        bits_string += '0' * (BYTE_SIZE - len(bits_string) % BYTE_SIZE)
    
    return bits_string, waste_bits

def write_bits_to_file(answer_file, bits_string):
    bytes_data = [bits_string[i:i+BYTE_SIZE] for i in range(0, len(bits_string), BYTE_SIZE)]
    bytes_data = [int(byte, 2) for byte in bytes_data]
    byte_array = struct.pack('B' * len(bytes_data), *bytes_data)
    
    answer_file.write(byte_array)

def get_positions():
    file_fai = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa.fai')
    start_chr_positions = [None] * 24
    for line in file_fai:

        splitted = line.split()
        chr_num = splitted[0][3:]
        if chr_num == 'X':
            chr_num = 23
        elif chr_num == 'Y':
            chr_num = 24

        chr_num = int(chr_num)
        lenght = int(splitted[1])
        row_length = int(splitted[3])
        with_sep_row_length = int(splitted[4])
        wit_sep_lenght = lenght + math.ceil(lenght / row_length) * (with_sep_row_length - row_length)
        start_chr_positions[chr_num-1]=Chromosome_Info(chr_num, int(splitted[2]), lenght, wit_sep_lenght, row_length, with_sep_row_length)

    return start_chr_positions


def preprocess_dna():
    df = pd.DataFrame(columns=['chr', 'start', 'byte_count', 'waste_bits'])
    file_fa = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa')
    answer_file = open(PREPROCESS_FILE, 'wb')
    start_chr_positions = get_positions()

    j = 0
    for i in tqdm(range(0, 5)):
        file_fa.seek(start_chr_positions[i].start_pos)
        line = file_fa.read(start_chr_positions[i].wit_sep_lenght)
        bits, waste_bits = convert_string_to_bits(line)
        df.loc[i] = [1, j, len(bits) // BYTE_SIZE, waste_bits]
        write_bits_to_file(answer_file, bits)
        j += len(bits) // BYTE_SIZE + 1
        df.to_csv(PREPROCESS_METADATA, index=False)


def read_bits_from_file(filepath, start, start_in_byte):
    file =  open(filepath, 'rb')
    file.seek(start)
    byte_array = file.read(NORM_WINDOW_SIZE)
    int_list = list(byte_array)
    
    bits_list = [format(byte, '08b') for byte in int_list][start_in_byte:WINDOW_SIZE]
    
    bits_string = ''.join(bits_list)
    return bits_string


def get_lines(chr : int, start : int):
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

def get_time():
    global WINDOW_SIZE 
    global NORM_WINDOW_SIZE
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 1000 * i
        NORM_WINDOW_SIZE = math.ceil(WINDOW_SIZE  * 3 / BYTE_SIZE)
        # print(WINDOW_SIZE)
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

    # start_time = time.time()
    # preprocess_dna()
    # # примерно 996.2882759571075 = 16 минут
    # res_time = time.time() - start_time
    # print(res_time)

    get_time()
    # G, T, A, C = get_lines(0, 170*60)
    # print(G)
    # print(T)
    # print(A)
    # print(C)




        
    

    
    