import pyBigWig
import h5py

# Указываем пути к файлам bigWig и HDF5
bigwig_file = 'interval.all.obs.bw'
hdf5_file = 'big_wig/bigwig.hdf5'

bw_file = pyBigWig.open(bigwig_file)
chromosomes = bw_file.chroms()
h5_file = h5py.File(hdf5_file, 'w')

j = 0
for chromosome, size in chromosomes.items():
    # if (chromosome == "chrY" or chromosome == "chrX" or int(chromosome[3:]) > 10):
    #     continue
    values = bw_file.values(chromosome, 0, size)
    print(chromosome)
    group = h5_file.create_dataset(chromosome, data=values)
    j += 1
    
bw_file.close()
h5_file.close()