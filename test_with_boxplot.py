import pandas as pd
import time
import random
import matplotlib.pyplot as plt
import seaborn as sns
from big_wig import get_bwlines_bw, get_hdf5lines_bw
from big_wig_hash_map import get_lines_bw_3
from bin_search_big_wig import get_lines_bwbs

functions = [get_hdf5lines_bw, get_bwlines_bw, get_lines_bw_3, get_lines_bwbs]
fun_name = ['hdf5', 'bw', 'hash map', 'bin search']


# сколько для каждого window size раз будет запускаться get_line
COUNT_PER_EACH_WINDOW_SIZE = 100
path_to_save_png = "resultlineplt.png"

def get_time():
    window_sizes = [[] for _ in range(len(functions))] 
    times = [[] for _ in range(len(functions))] 
    for i in range(1, 100000):
        WINDOW_SIZE = i * 10
        print(WINDOW_SIZE)
        
        fun_num = 0
        for fun in functions:
            for _ in range(0, COUNT_PER_EACH_WINDOW_SIZE):
                start_time = time.time()
                start_pos = random.randint(0, 20000000)
                chr = random.randint(0, 0)
                ans = fun(chr, start_pos, WINDOW_SIZE)
                len_ans = len(ans)
                res_time = time.time() - start_time
                window_sizes[fun_num].append(WINDOW_SIZE)
                times[fun_num].append(res_time)
            fun_num += 1
        
    
    return window_sizes, times

def test_bw():
    window_sizes, times = get_time()

    all_data = [{'window_size':  window_sizes[i], 'time': times[i]} for i in range(len(functions))]
    all_data_frames = [pd.DataFrame(all_data[i]) for i in range(len(functions))]
    
    sns.lineplot(data=all_data_frames[0], x="window_size", y="time", orient="x", label='hdf5')
    sns.lineplot(data=all_data_frames[1], x="window_size", y="time", orient="x", color="black", label='bw')
    sns.lineplot(data=all_data_frames[2], x="window_size", y="time", orient="x", color="#F72585", label='hash map')
    sns.lineplot(data=all_data_frames[3], x="window_size", y="time", orient="x", color="#4CC9F0", label='bin search')
    plt.legend()

    plt.savefig(path_to_save_png)


if __name__ == '__main__':
    test_bw()
