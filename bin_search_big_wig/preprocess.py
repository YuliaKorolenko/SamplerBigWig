import pyBigWig
import math
import numpy as np
import os
import sys

# you can select any value from the segment -> [1...24], max - 24
size_of_bw = 1

# Открываем bigWig файл для чтения
file_path = "file_paths.txt"
output_folder = "bnbigwig"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

def preprocess():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    file_paths = []
    with open(file_path, 'r') as file:
        for line in file:
            file_paths.append(line.strip())

    for filename in file_paths:
        if filename.endswith(".bw"):
            print("current file: ", filename)
            bw_path = os.path.join(filename)

            bw = pyBigWig.open(bw_path)
            positions = []
            values_ziped = []

            j = 0
            for i in range(1, size_of_bw + 1):
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

                values = bw.values(chr, 0, chrom_size)

                for pos, value in enumerate(values, start=1):
                    if not math.isnan(value):
                        positions.append(pos + j)
                        values_ziped.append(value)
                        break
                        
                j += chrom_size
            
            
            file_basename = os.path.basename(filename)
            output_path = os.path.join(output_folder, file_basename.replace(".bw", "_data"))
            np.save(output_path + '_positions.npy', np.array(positions, dtype=np.int64))
            np.save(output_path + '_values.npy', np.array(values_ziped, dtype=np.int64))
            
            bw.close()


if __name__ == '__main__':
    preprocess()
