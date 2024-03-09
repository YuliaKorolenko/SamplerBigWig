import pyBigWig
import math
import pandas as pd
from dataclasses import dataclass
import os

PREPROCESS_METADATA = "bin_array/bin_metadata.csv"
df = pd.read_csv(PREPROCESS_METADATA)

def get_chr_name_for_bw(i : int):
    chr_num = 'chr%s' % (i + 1)
    if i == 22:
        chr_num = 'chrY'
    elif i == 23:
        chr_num = 'chrX'
    return chr_num

def get_bw_vector(i : int, start : int, WINDOW_SIZE : int):
    chr_num = get_chr_name_for_bw(i)

    folder_path = "foldbigwig"
    result_vector = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".bw"):
            bigwig_file = os.path.join(folder_path, filename)
            bigwig = pyBigWig.open(bigwig_file)
            
            chrom_sizes = bigwig.chroms()
            from_bound = start
            to_bound = start + WINDOW_SIZE
            if (chrom_sizes[chr_num] < to_bound):
                to_bound = chrom_sizes[chr_num]
            if (chrom_sizes[chr_num] > from_bound):
                bw_values = bigwig.values(chr_num, from_bound, to_bound)  # Пример, можно использовать любой хромосомный регион
                result_vector.append(bw_values)
            else:
                result_vector.append([])

            bigwig.close()
    
    return result_vector


if __name__ == '__main__':
    print(get_bw_vector(0, 0, 10))
    # file_path = 'interval.all.obs.bw'
    # bw_file = pyBigWig.open(file_path)
    # chromosomes = bigwig.chroms()
    # chromosome_name = 'chrY'

    # if chromosome_name in chromosomes:
    #     chromosome_size = chromosomes[chromosome_name]
    #     print(f"Количество элементов в хромосоме {chromosome_name}: {chromosome_size}")
    # else:
    #     print(f"Хромосома {chromosome_name} не существует в файле bigWig")