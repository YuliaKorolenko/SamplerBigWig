import time
import random
import matplotlib.pyplot as plt
from less_memory import get_lines as get_lines_1
from less_memory_2_try import get_lines as get_lines_2
from read_byte import get_lines as get_lines_3

functions = [get_lines_1, get_lines_2, get_lines_3]

def get_time():
    global WINDOW_SIZE 
    times = [[] for _ in range(len(functions))]
    sizes = []
    for i in range(1, 10):
        WINDOW_SIZE = 1000 * i

        print(WINDOW_SIZE)
        # print(NORM_WINDOW_SIZE)
        fun_num = 0
        for fun in functions:
            start_time = time.time()
            for _ in range(0, 1000):
                start_pos = random.randint(0, 20000000)
                chr = random.randint(0, 23)
                ans = fun(chr, start_pos, WINDOW_SIZE)
        
            res_time = time.time() - start_time
            times[fun_num].append(res_time)
            print("--- %s seconds ---" % res_time)
            fun_num += 1
        sizes.append(WINDOW_SIZE)

    plt.ylabel('Time in seconds')
    plt.xlabel('Window size') 
    print(sizes)
    plt.plot(sizes, times[0], color='pink', label='less memory')
    plt.plot(sizes, times[1], color='purple', label='less memory 2 try')
    plt.plot(sizes, times[2], color='blue', label='read byte')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    get_time()
    # print(get_lines_2(0, 0))