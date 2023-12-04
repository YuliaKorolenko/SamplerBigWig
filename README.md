# SamplerBigWig

less_memory там, где разными способами пробую считывать с файла в который записываю в битах. Есть свой preprocess. Надо запустить перед использованием.

bin_files - тут попытка записывать 4 one_hot вектора в binary file и работа с ними. Но DNA тогда получается размером 38gb. Тоже есть свой preprocess

main - работа c обычным HOMO_sapiens....

numpy_arr - сохранение 4 numpy array. Если переводить 10 хромосом, то каждый из 4 numpy array займет 13 gb
![Alt text](image.png)

## DNA

| Tool        | hdf5    | #2    |
| :---:       | :---:   | :---: |
| Size in GB  | 93.57   | 283   |
| :---:       | :---:   | :---: |
| Time in min | 94      | 283   |
16:07 - 3 хром
