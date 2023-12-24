import pyBigWig
import math
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt

bigwig_file = 'interval.all.obs.bw'
bigwig = pyBigWig.open(bigwig_file)

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


if __name__ == '__main__':
    start_chr_positions = get_positions()

    ans = []
    all_numbers = 0

    Ysize = 1000000

    for i in range(0, 1):
        chr_num = 'chr%s' % (i + 1)
        print(chr_num)
        values = bigwig.values(chr_num, 0, start_chr_positions[i].lenght)
        j = 0
        i = 0
        k = 0
        cur = 0

        for value in values:
            all_numbers += 1
            if not math.isnan(value):
                i += 1
                cur += 1
            else :
                k += 1
            j += 1
            if (all_numbers % Ysize == 0):
                print(cur)
                ans.append(cur)
                cur = 0

        print("percent", i * 100 / j)

    x = [i*Ysize for i in range(0, len(ans))]
    print(x)
    plt.plot(x, ans)
    plt.ylim(0, 1000000)
    plt.show()

    print("все значения", all_numbers)
