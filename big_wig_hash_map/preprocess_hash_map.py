import pyBigWig
import math
import os
import sys

# you can select any value from the segment -> [1...24], max - 24
size_of_bw = 1

file_path = "file_paths.txt"
res_folder_path = "hashmapfold"

def prerpocess_all():
    if not os.path.exists(res_folder_path):
        os.makedirs(res_folder_path)
    file_paths = []
    with open(file_path, 'r') as file:
        for line in file:
            file_paths.append(line.strip())
    i = 0        
    for file_name in file_paths:
        print(file_name)
        preprocess_bw(file_name, i)
        i += 1

def preprocess_bw(file_name, cnt):
    print("current file: ", file_name)
    bw = pyBigWig.open(file_name)

    data_map = {}

    bw_size = bw.header()['nBasesCovered']
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
                data_map[j + pos] = value

        j += chrom_size

    bw.close()

    # Сохраняем хеш-таблицу в файл
    file_basename = os.path.basename(file_name)
    output_path = os.path.join(res_folder_path, file_basename.replace(".bw", "_hm.txt"))
    with open(output_path, "w") as file:
        for key, value in data_map.items():
            file.write(str(key) + "\t" + str(value) + "\n")

if __name__ == '__main__':
    print(prerpocess_all())
