import pyBigWig
import math
import os

# you can select any value from the segment -> [1...24]
size_of_bw = 3

folder_path = "foldbigwig"
res_folder_path = "resfoldbigwig"
files_list = []

def prerpocess_all():
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files_list = os.listdir(folder_path)
        i = 0
        for file in files_list:
            print(os.path.join(folder_path, file))
            preprocess_bw(os.path.join(folder_path, file), i)
            i += 1

def preprocess_bw(file_name, cnt):
    bw = pyBigWig.open(file_name)

    data_map = {}

    bw_size = bw.header()['nBasesCovered']
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
                data_map[j + pos] = value

        j += chrom_size

    # Закрываем файл
    bw.close()

    # Сохраняем хеш-таблицу в файл
    with open("resfoldbigwig/info_%s.txt" % cnt, "w") as file:
        for key, value in data_map.items():
            file.write(str(key) + "\t" + str(value) + "\n")

if __name__ == '__main__':
    print(prerpocess_all())
