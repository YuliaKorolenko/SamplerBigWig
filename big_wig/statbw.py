
import pyBigWig
import math
import pandas as pd
from dataclasses import dataclass
import matplotlib.pyplot as plt

bigwig_file = 'interval.all.obs.bw'
bigwig = pyBigWig.open(bigwig_file)

if __name__ == '__main__':
    # Открытие файла bigWig
    bw = pyBigWig.open("interval.all.obs.bw")

    # Получение всех хромосом из файла
    chromosomes = bw.chroms()

    chromosomes = bigwig.chroms()

    ans = []
    all_numbers = 0
    from_ = 17438425
    to_ = 17438425 + 20

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
                # print(all_numbers)
                if (all_numbers >= from_ and all_numbers < to_):
                    ans.append(1)
                    print(all_numbers)
            else :
                k += 1
                if (all_numbers >= from_ and all_numbers < to_):
                    ans.append(0)
            j += 1

        print("percent", l * 100 / j)
        break

    x = [i for i in range(from_, to_)]
    print(x)
    print(ans)
    print(len(x))
    print(len(ans))
    plt.scatter(x, ans)
    plt.show()