import h5py
import os

hdf5_folder = 'hdf5bigwig'

def load_hdf5_files(hdf5_folder):
    hdf5_files = []
    
    for filename in os.listdir(hdf5_folder):
        hdf5_files.append(h5py.File(os.path.join(hdf5_folder, filename), 'r'))
    
    return hdf5_files


hdf5_files = load_hdf5_files(hdf5_folder)

def get_h5_vector(chr : int, start : int, WINDOW_SIZE : int):
    vectors_all = []
    
    for hdf5_file in hdf5_files:
        vectors = get_vector(chr, start, WINDOW_SIZE, hdf5_file)
        vectors_all.append(vectors)
    
    return vectors_all

def get_vector(i, start, WINDOW_SIZE, hdf5_file):
    chr_num = 'chr%s' % (i + 1)
    if i == 22:
        chr_num = 'chrY'
    elif i == 23:
        chr_num = 'chrX'
    return hdf5_file[chr_num][start :start + WINDOW_SIZE]


if __name__ == '__main__':
    print(get_h5_vector(1, 53533, 1000))

    # # Открываем файл HDF5 для чтения данных
    # hdf5_file = h5py.File('big_wig/bigwig.hdf5', 'r')

    # group_name = 'chr1'
    # dataset_name = 'values'

    # start_index = 10
    # end_index = 20
    # data = hdf5_file[dataset_name][start_index:end_index]

    # print(data)

    # hdf5_file.close()