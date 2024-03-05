from clickhouse_driver import Client
import os
import pyBigWig

bw_folder = "foldbigwig"
size_of_bw = 1

# client = Client(host='localhost')

# print(client.execute('SELECT * FROM system.numbers LIMIT 5'))

# # client.execute(
# #     'INSERT INTO test (x) VALUES',
# #     ((x, ) for x in range(5))
# # )

# # print(client.execute('SELECT * FROM test'))

# # client.execute(
# # 'CREATE TABLE myThirdReplacingMT(`key` Int64,`chr1` Nullable(Int64)) ENGINE = ReplacingMergeTree ORDER BY key;'
# # )

# tables = client.execute('SHOW TABLES')
# for i in tables:
#     print("table ", i)


# arr_cur = [None, 1, 3, -999, 3, 4, 5]
# # # kkk = list((x, arr_cur[x]) for x in range(7))
# # # print(kkk)

# client.execute(
#     'INSERT INTO myThirdReplacingMT (key, chr1) VALUES',
#     ((x, arr_cur[x], ) for x in range(7))
# )

# print(client.execute('SELECT * FROM myThirdReplacingMT'))


def preprocess():
    client = Client(host='localhost')

    for filename in os.listdir(bw_folder):
        if filename.endswith(".bw"):
            bw_path = os.path.join(bw_folder, filename)
            print(bw_path)

        # bw = pyBigWig.open(bw_path)

        client.execute('DROP TABLE IF EXISTS my4ReplacingMT')

        client.execute(
        'CREATE TABLE my4ReplacingMT(`key` Int64,`chr1` Nullable(Int64)) ENGINE = ReplacingMergeTree ORDER BY key;'
        )

        current_size = 0
        for i in range(1, size_of_bw + 1):
            chr = "chr"
            if i == 23:
                chr += "X"
            elif i == 24:
                chr += "Y"
            else:
                chr += str(i)
            print(chr)

            # Получаем размер хромосомы
            # chrom_size = bw.chroms(chr)
            # print("chrom_size ", chrom_size)

            # values = bw.values(chr, 0, chrom_size)

            elements = [None] * len(20)
            # print(elements)

            # elements = []

            # for pos, value in enumerate(values, start=1):
            #     current_size += 1
            #     # print(pos, value)
            #     elements.append(value)
            #     break
            
            print(elements)

            client.execute(
                'INSERT INTO my4ReplacingMT (key, chr1) VALUES',
                ((x, elements[x], ) for x in range(len(elements)))
            )
        
        bw.close()

    print(client.execute('SELECT * FROM my4ReplacingMT'))

            


if __name__ == '__main__':
    preprocess()

