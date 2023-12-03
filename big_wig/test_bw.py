import math
import random
import matplotlib.pyplot as plt
import time
from read_bw import get_bw_vector
from read_hdf5 import get_h5_vector

def get_time():
    times_bw = []
    times_h5 = []
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 100000 * i
        print(WINDOW_SIZE)
        start_time_bw = time.time()
        for _ in range(0, 10000):
            chr = random.randint(0, 9)
            start_pos = random.randint(0, 2000000)
            bw = get_bw_vector(chr, start_pos, WINDOW_SIZE)

        res_time_bw = time.time() - start_time_bw
        times_bw.append(res_time_bw)

        start_time_h5 = time.time()
        for _ in range(0, 10000):
            chr = random.randint(0, 9)
            start_pos = random.randint(0, 2000000)
            bw = get_h5_vector(chr, start_pos, WINDOW_SIZE)
        
        res_time_h5 = time.time() - start_time_h5
        times_h5.append(res_time_h5)

        sizes.append(WINDOW_SIZE)
        print("--- %s seconds hdf5 ---" % res_time_h5)
        print("--- %s seconds big wig ---" % res_time_bw)
    plt.xlabel('Window size')
    plt.ylabel('Time in seconds') 
    plt.title('With the current window size, we request a sub-section 1000 times')
    plt.plot(sizes, times_h5, color='pink', label='hdf5')
    plt.plot(sizes, times_bw, color='skyblue', label='big wig')   
    plt.legend()
    plt.show()
    return

if __name__ == '__main__':
    get_time()