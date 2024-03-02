import pyBigWig
import math
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt

bigwig_file = 'interval.all.obs.bw'
bigwig = pyBigWig.open(bigwig_file)

if __name__ == '__main__':
    # # Открытие файла bigWig
    # bw = pyBigWig.open("interval.all.obs.bw")

    # # Получение всех хромосом из файла
    # chromosomes = bw.chroms()

    # # Вывод всех хромосом
    # for chromosome in chromosomes:
    #     print(chromosome)

    ans = []
    all_numbers = 0
    to_chr = 24

    chromosomes = bigwig.chroms()

    # Считывание значений для каждой хромосомы
    for chromosome, size in chromosomes.items():
        values = bigwig.values(chromosome, 0, size)
        print(f"Chromosome: {chromosome}")
        j = 0
        l = 0
        k = 0
        for value in values:
            all_numbers += 1
            if not math.isnan(value):
                l += 1
            else :
                k += 1
            j += 1

        ans.append(l * 100 / j)

        print("percent", l * 100 / j)
    
    x = [i for i in range(1, to_chr + 1)]
    print(x)
    print(ans)
    # plt.plot(x, ans)
    # Разукрашивание области под линией
    plt.fill_between(x, ans, color='lightblue')

    # Разукрашивание области над линией
    plt.fill_between(x, ans, 100, color='lightcoral')
    plt.ylim(0, 100)
    plt.show()

    print("все значения", all_numbers)