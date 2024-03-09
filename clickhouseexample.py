from clickhouse_driver import Client
import os
import pyBigWig
import math
from big_wig import get_bwlines_bw

bw_folder = "foldbigwig"
size_of_bw = 1
WINDOW_PREPROCESS = 1000000

client = Client(host='localhost')

def prepare_for_insert(arr_before_prep):
    ans = []
    for arr_i in arr_before_prep:
        cur_arr = []
        for j in arr_i:
            if math.isnan(j):
                cur_arr.append(None)
            else:
                cur_arr.append(int(j))
        ans.append(cur_arr)
    return ans


def preprocess_all():
    client = Client(host='localhost')
    client.execute('DROP TABLE IF EXISTS my4ReplacingMT')

    client.execute(
    'CREATE TABLE my4ReplacingMT(`key` Int64,`chr0` Nullable(Int64),`chr1` Nullable(Int64),' +
    '`chr2` Nullable(Int64),`chr3` Nullable(Int64),`chr4` Nullable(Int64)) ENGINE = ReplacingMergeTree ORDER BY key;'
    )

    last_array_size = WINDOW_PREPROCESS
    prev_chr_size = 0
    # пока для одной хромосомы

    for i in range(0, size_of_bw):
        cur_start = 0
        while last_array_size == WINDOW_PREPROCESS:
            print(cur_start)
            ans = get_bwlines_bw(i, cur_start, WINDOW_PREPROCESS)
            last_array_size = len(ans[0])
            # last_array_size = 0
            after_prep = prepare_for_insert(ans)

            insert_string = 'INSERT INTO my4ReplacingMT (key, chr0, chr1, chr2, chr3, chr4) VALUES'
            client.execute(
                insert_string,
                ((x + cur_start, after_prep[0][x], after_prep[1][x], after_prep[2][x], after_prep[3][x], after_prep[4][x]) 
                for x in range(len(after_prep[0])))
            )
            cur_start += WINDOW_PREPROCESS


    print("select:")
    print(client.execute('SELECT count(*) FROM my4ReplacingMT'))

def select_count():
    print("select count:")
    print(client.execute('SELECT count(*) FROM my4ReplacingMT'))

def get_line(i : int, start : int, WINDOW_SIZE : int):
    return(client.execute("SELECT * FROM my4ReplacingMT where key >= %d and key < %d" % (start, start + WINDOW_SIZE)))


if __name__ == '__main__':
    print(get_line(0, 0, 10))
    # select_count()
    # client = Client(host='localhost')
    # answer = client.execute('SELECT chr1 FROM my4ReplacingMT WHERE key > 10 and key < 30')
    # for i in answer:
    #     print(i[0])

