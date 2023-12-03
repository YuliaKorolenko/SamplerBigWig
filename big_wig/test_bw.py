import math
import random
import matplotlib.pyplot as plt
import time
from read_bw import get_bw_vector

def get_time():
    times = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 100000 * i
        print(WINDOW_SIZE)
        start_time = time.time()
        for _ in range(0, 10000):
            chr = random.randint(0, 23)
            start_pos = random.randint(0, 2000000)
            bw = get_bw_vector(chr, start_pos, WINDOW_SIZE)
        
        res_time = time.time() - start_time
        times.append(res_time)
        sizes.append(WINDOW_SIZE)
        print("--- %s seconds ---" % res_time)
    plt.xlabel('Time in seconds')
    plt.ylabel('Window size')    
    plt.plot(times, sizes,'ro')
    plt.show()

if __name__ == '__main__':
    get_time()