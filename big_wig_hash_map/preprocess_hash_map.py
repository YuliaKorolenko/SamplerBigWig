import pyBigWig
import math

# you can select any value from the segment -> [1...24]
size_of_bw = 24

# Открываем bigWig файл для чтения
bw = pyBigWig.open("interval.all.obs.bw")

# Создаем пустую хеш-таблицу для хранения ненулевых значений
data_map = {}

# Получаем размер bigWig файла
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
with open("big_wig_hash_map/data_map.txt", "w") as file:
    for key, value in data_map.items():
        file.write(str(key) + "\t" + str(value) + "\n")