import pyBigWig
import math
import numpy as np

# you can select any value from the segment -> [1...24]
size_of_bw = 24

# Открываем bigWig файл для чтения
bw = pyBigWig.open("interval.all.obs.bw")

def preprocess():
    # Получаем размер bigWig файла
    positions = []
    values_ziped = []

    j = 0
    for i in range(1, size_of_bw):
        chr = "chr"
        if i == 23:
            chr += "X"
        elif i == 24:
            chr += "Y"
        else:
            chr += str(i)
        print(chr)

        # Получаем размер хромосомы
        chrom_size = bw.chroms(chr)
        print("chrom_size ", chrom_size)
        print("j ", j)

        values = bw.values(chr, 0, chrom_size)

        for pos, value in enumerate(values, start=1):
            if not math.isnan(value):
                positions.append(pos + j)
                values_ziped.append(value)
                
        j += chrom_size
    
    np.save('bin_search_big_wig/positions', np.array(positions, dtype=np.int64))
    np.save('bin_search_big_wig/values_ziped', np.array(values_ziped, dtype=np.int64))

if __name__ == '__main__':
    preprocess()
