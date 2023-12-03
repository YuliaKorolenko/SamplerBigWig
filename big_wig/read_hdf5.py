import h5py

hdf5_file = h5py.File('big_wig/bigwig.hdf5', 'r')

def get_h5_vector(i, start, WINDOW_SIZE):
    chr_num = 'chr%s' % (i + 1)
    if i == 22:
        chr_num = 'chrY'
    elif i == 23:
        chr_num = 'chrX'
    return hdf5_file[chr_num][start :start + WINDOW_SIZE]


if __name__ == '__main__':
    print(get_h5_vector(8, 53533, 1000))

    # # Открываем файл HDF5 для чтения данных
    # hdf5_file = h5py.File('big_wig/bigwig.hdf5', 'r')

    # group_name = 'chr1'
    # dataset_name = 'values'

    # start_index = 10
    # end_index = 20
    # data = hdf5_file[dataset_name][start_index:end_index]

    # print(data)

    # hdf5_file.close()