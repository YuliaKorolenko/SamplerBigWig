from bitarray import bitarray
from dataclasses import dataclass
from tqdm import tqdm
import pandas as pd
import math
import numpy as np
import os

# 000 - T
# 001 - C
# 010 - A
# 011 - G
# 100 - N


A_FILE = "bin_array/A"
C_FILE = "bin_array/C"
G_FILE = "bin_array/G"
T_FILE = "bin_array/T"
PREPROCESS_METADATA = "bin_array/bin_metadata.csv"

@dataclass
class Chromosome_Info:
    number: int
    start_pos: int
    lenght: int
    wit_sep_lenght : int
    row_length : int
    with_sep_row_length : int

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

def to_one_hot(lines : str, cur_size : int):
    j = 0
    G = [0] * cur_size
    T = [0] * cur_size
    A = [0] * cur_size
    C = [0] * cur_size
    for i in lines:
        if (i == 'G'):
            G[j] = 1
        elif (i == 'T'):
            T[j] = 1
        elif (i == 'A'):
            A[j] = 1
        elif (i == 'C'):
            C[j] = 1
        elif (i != 'N'):
            continue
        j += 1
    return G, T, A, C

def preprocess_dna():
    bitarray_empty = bitarray()

    with open(A_FILE, 'wb') as file1:
        bitarray_empty.tofile(file1)

    with open(C_FILE, 'wb') as file2:
        bitarray_empty.tofile(file2)

    with open(G_FILE, 'wb') as file3:
        bitarray_empty.tofile(file3)
        
    with open(T_FILE, 'wb') as file4:
        bitarray_empty.tofile(file4)

    df = pd.DataFrame(columns=['start', 'lenght'])
    file_fa = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa')
    start_chr_positions = get_positions()

    j = 0
    for i in tqdm(range(0, 24)):
        file_fa.seek(start_chr_positions[i].start_pos)
        line = file_fa.read(start_chr_positions[i].wit_sep_lenght - 1)

        G, T, A, C = to_one_hot(line, start_chr_positions[i].wit_sep_lenght - 1)

        df.loc[i] = [j, start_chr_positions[i].wit_sep_lenght - 1]
        j += start_chr_positions[i].wit_sep_lenght - 1
        df.to_csv(PREPROCESS_METADATA, index=False)

        file_size = os.path.getsize(A_FILE)
        ans_A = bitarray(A)
        with open(A_FILE, 'r+b') as file:
            file.seek(file_size)
            ans_A.tofile(file) 

        ans_C = bitarray(C)
        with open(C_FILE, 'r+b') as file:
            file.seek(file_size)
            ans_C.tofile(file) 

        ans_G = bitarray(G)
        with open(G_FILE, 'r+b') as file:
            file.seek(file_size)
            ans_G.tofile(file) 

        ans_T = bitarray(T)
        with open(T_FILE, 'r+b') as file:
            file.seek(file_size)
            ans_T.tofile(file) 


if __name__ == '__main__':
    preprocess_dna()
