import pyBigWig
import math
import pandas as pd
from dataclasses import dataclass

bigwig_file = 'interval.all.obs.bw'
bigwig = pyBigWig.open(bigwig_file)

def get_bw_vector(i : int, start : int, WINDOW_SIZE : int):
    chr_num = 'chr%s' % (i + 1)
    if i == 22:
        chr_num = 'chrY'
    elif i == 23:
        chr_num = 'chrX'
    return bigwig.values(chr_num, start, start + WINDOW_SIZE)


if __name__ == '__main__':
    print(get_bw_vector(22, 53533, 1000))
    # file_path = 'interval.all.obs.bw'
    # bw_file = pyBigWig.open(file_path)
    # chromosomes = bigwig.chroms()
    # chromosome_name = 'chrY'

    # if chromosome_name in chromosomes:
    #     chromosome_size = chromosomes[chromosome_name]
    #     print(f"Количество элементов в хромосоме {chromosome_name}: {chromosome_size}")
    # else:
    #     print(f"Хромосома {chromosome_name} не существует в файле bigWig")