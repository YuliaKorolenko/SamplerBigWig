import pyBigWig
import math
import numpy as np
import os

# you can select any value from the segment -> [1...24]
size_of_bw = 2

# Открываем bigWig файл для чтения
bw_folder = "foldbigwig"
output_folder = "bnbigwig"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def preprocess():
    for filename in os.listdir(bw_folder):
        if filename.endswith(".bw"):
            bw_path = os.path.join(bw_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".bw", "_data"))

            bw = pyBigWig.open(bw_path)
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
            
            np.save(output_path + '_positions.npy', np.array(positions, dtype=np.int64))
            np.save(output_path + '_values.npy', np.array(values_ziped, dtype=np.int64))
            
            bw.close()

if __name__ == '__main__':
    preprocess()
