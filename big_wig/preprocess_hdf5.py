import pyBigWig
import h5py
import os


bigwig_folder = 'foldbigwig'
output_folder = 'hdf5bigwig' 
file_path = 'file_paths.txt'
size_of_bw = 1

def get_ch_number(chromosome):
    if (chromosome == "chrY"):
        return 23
    if (chromosome == "chrX"):
        return 24
    return int(chromosome[3:])


def prerpocess_all():
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    file_paths = []
    with open(file_path, 'r') as file:
        for line in file:
            file_paths.append(line.strip())
    for file_name in file_paths: 
        if file_name.endswith('.bw'): 
            print("current file: ", file_name)
            bw_file = pyBigWig.open(file_name)
            chromosomes = bw_file.chroms()

            file_basename = os.path.basename(file_name)
            h5_file = h5py.File(os.path.join(output_folder, file_basename[:-3] + 'h5'), 'w')

            for chromosome, size in chromosomes.items():
                if (get_ch_number(chromosome) > size_of_bw):
                    continue
                print(chromosome)
                values = bw_file.values(chromosome, 0, size)
                group = h5_file.create_dataset(chromosome, data=values)

            bw_file.close()
            h5_file.close()

if __name__ == '__main__':
    print(prerpocess_all())