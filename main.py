import time
from dataclasses import dataclass
import math
import random
import matplotlib.pyplot as plt
from less_memory import get_lines_1


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

NUMBER_IN_LINE = 60
# WINDOW_SIZE = 10
start_chr_positions = get_positions()


def get_location(chr_info : Chromosome_Info, start, WINDOW_SIZE : int):
    assert start >= 0, 'Start position must be non-negative'

    diff = chr_info.with_sep_row_length - chr_info.row_length
    start_pos = chr_info.start_pos + start +  start // chr_info.row_length * diff
    lengh_window =  WINDOW_SIZE + (WINDOW_SIZE + start % chr_info.row_length) // chr_info.row_length * diff
    end_pos = start_pos + lengh_window

    assert end_pos <= chr_info.start_pos + chr_info.wit_sep_lenght , 'Make the starting position smaller or choose a different chromosome'

    return start_pos, lengh_window

def to_one_hot(lines : str, WINDOW_SIZE : int):
    j = 0
    G = [0] * WINDOW_SIZE
    T = [0] * WINDOW_SIZE
    A = [0] * WINDOW_SIZE
    C = [0] * WINDOW_SIZE
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


# the starting position is included inclusive
def get_lines(chr_number : int, start_pos : int, WINDOW_SIZE : int):
    file_fa = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa')

    start_pos, lengh_window = get_location(start_chr_positions[chr_number], start_pos, WINDOW_SIZE)

    file_fa.seek(start_pos, 0)
    lines = file_fa.read(lengh_window).replace("\n", "")
    assert len(lines) == WINDOW_SIZE, 'MISTAKE'
        

    return to_one_hot(lines, WINDOW_SIZE)



def get_time():
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 1000 * i
        start_time = time.time()
        for _ in range(0, 10000):
            chr = random.randint(0, 23)
            start_pos = random.randint(0, 20000000)
            G, T, A, C = get_lines(chr, start_pos, WINDOW_SIZE)
        
        res_time = time.time() - start_time
        times.append(res_time)
        sizes.append(WINDOW_SIZE)
        print("--- %s seconds ---" % res_time)
    plt.xlabel('Time in seconds')
    plt.ylabel('Window size')    
    plt.plot(times, sizes,'ro')
    plt.show()



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    file_fai = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa.fai')
    file_fa = open('Homo_sapiens.GRCh38.dna.primary_assembly.fa')
    
    # get_time()
    G, T, A, C = get_lines(0, 170*60, 111)
    print(G)
    print(T)
    print(A)
    print(C)
