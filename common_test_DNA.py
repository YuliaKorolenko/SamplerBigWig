import time
import random
import matplotlib.pyplot as plt
from less_memory import get_lines_1, get_lines_2
from hdf5 import get_lines_4
from bin_files import get_lines_5
from numpy_arr import get_lines_6
from main import get_lines as get_lines_7
from bin_array import get_lines_8

functions = [get_lines_4, get_lines_5, get_lines_6, get_lines_7, get_lines_8]

def get_time():
    global WINDOW_SIZE 
    times = [[] for _ in range(len(functions))]
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 100000 * i
        print(WINDOW_SIZE)
        
        fun_num = 0
        for fun in functions:
            start_time = time.time()
            for _ in range(0, 1000):
                start_pos = random.randint(0, 20000000)
                chr = random.randint(0, 1)
                ans = fun(chr, start_pos, WINDOW_SIZE)
        
            res_time = time.time() - start_time
            times[fun_num].append(res_time)
            print("--- %s seconds ---" % res_time)
            fun_num += 1
        sizes.append(WINDOW_SIZE)

    plt.ylabel('Time in seconds')
    plt.xlabel('Window size') 
    print(sizes)
    # plt.plot(sizes, times[0], color='black', label='less memory')
    # plt.plot(sizes, times[1], color='purple', label='less memory 2 try')
    plt.plot(sizes, times[0], color="#F72585", label='hdf5')
    plt.plot(sizes, times[1], color="#7209B7", label='bin files')
    plt.plot(sizes, times[2], color="#4361EE", label='numpy arr')
    plt.plot(sizes, times[3], color="#4CC9F0", label='simple')
    plt.plot(sizes, times[4], color='#4361EE', label='bin files')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    get_time()

    # print(get_lines_4(0, 0, 10))