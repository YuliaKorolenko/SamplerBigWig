import pyBigWig
import h5py
import os


output_folder = 'hdf5bigwig' 
if not os.path.exists(output_folder): os.makedirs(output_folder)

# bw_file = pyBigWig.open(bigwig_file)
# chromosomes = bw_file.chroms()
# h5_file = h5py.File(hdf5_file, 'w')

# j = 0
# for chromosome, size in chromosomes.items():
#     # if (chromosome == "chrY" or chromosome == "chrX" or int(chromosome[3:]) > 10):
#     #     continue
#     values = bw_file.values(chromosome, 0, size)
#     print(chromosome)
#     group = h5_file.create_dataset(chromosome, data=values)
#     j += 1
    
# bw_file.close()
# h5_file.close()


bigwig_folder = 'foldbigwig'

for root, dirs, files in os.walk(bigwig_folder):
     for file in files: 
        if file.endswith('.bw'): 
            bw_file = pyBigWig.open(os.path.join(root, file))
            chromosomes = bw_file.chroms()

            h5_file = h5py.File(os.path.join(output_folder, file[:-3] + 'h5'), 'w')

            for chromosome, size in chromosomes.items():
                if (chromosome == "chrY" or chromosome == "chrX" or int(chromosome[3:]) > 2):
                    continue
                values = bw_file.values(chromosome, 0, size)
                group = h5_file.create_dataset(chromosome, data=values)

            bw_file.close()
            h5_file.close()