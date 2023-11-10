from tqdm import tqdm
import struct
from dataclasses import dataclass
import math
import pandas as pd

PREPROCESS_FILE = "DNA"
PREPROCESS_METADATA = "metadata.csv"
BYTE_SIZE = 8

# Словарь для сопоставления символов с битовым представлением
bit_mapping = {
    'T': '001',
    'C': '010',
    'G': '011',
    'A': '100',
    'N': '000'
}

@dataclass
class Chromosome_Info:
    number: int
    start_pos: int
    lenght: int
    wit_sep_lenght : int
    row_length : int
    with_sep_row_length : int

def preprocess_dna():
    df = pd.DataFrame(columns=['start', 'byte_count', 'waste_bits'])
    file_fa = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa')
    answer_file = open(PREPROCESS_FILE, 'wb')
    start_chr_positions = get_positions()

    j = 0
    for i in tqdm(range(0, 24)):
        file_fa.seek(start_chr_positions[i].start_pos)
        line = file_fa.read(start_chr_positions[i].wit_sep_lenght)
        bits, waste_bits = convert_string_to_bits(line)
        df.loc[i] = [j, len(bits) // BYTE_SIZE, waste_bits]
        write_bits_to_file(answer_file, bits)
        j += len(bits) // BYTE_SIZE + 1
        df.to_csv(PREPROCESS_METADATA, index=False)

def write_bits_to_file(answer_file, bits_string):
    bytes_data = [bits_string[i:i+BYTE_SIZE] for i in range(0, len(bits_string), BYTE_SIZE)]
    bytes_data = [int(byte, 2) for byte in bytes_data]
    byte_array = struct.pack('B' * len(bytes_data), *bytes_data)
    
    answer_file.write(byte_array)


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


if __name__ == '__main__':
    # start_time = time.time()
    # when you do preprocess, comment out 21th line => df = pd.read_csv(PREPROCESS_METADATA)
    preprocess_dna()
    # # примерно 996.2882759571075 = 16 минут
    # res_time = time.time() - start_time
    # print(res_time)