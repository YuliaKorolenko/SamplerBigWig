import h5py
import numpy as np

# Создание массивов
arr1 = np.array([1, 2, 3, 4, 5])
arr2 = np.random.random((3, 3))
arr3 = np.arange(10)
arr4 = np.linspace(0, 1, 100)

# Запись массивов в файл HDF5
with h5py.File('data.h5', 'w') as f:
    f.create_dataset('array1', data=arr1)
    f.create_dataset('array2', data=arr2)
    f.create_dataset('array3', data=arr3)
    f.create_dataset('array4', data=arr4)