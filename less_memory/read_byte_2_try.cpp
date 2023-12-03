#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <sstream>
using namespace std;

std::ifstream inputFile;
int BYTE_SIZE = 8;

struct Data {
    int start;
    int byte_count;
    int waste_bits;
};

std::vector<Data> metadata;

int get_next(int &cur_pos_in_byte, int &byte_num){
    if (cur_pos_in_byte >= BYTE_SIZE){
        byte_num++;
        cur_pos_in_byte = 0;
    }
    cur_pos_in_byte++;
    return cur_pos_in_byte - 1;
}

vector<int> get_one_hot(int start, int start_in_byte, int WINDOW_SIZE){
    std::ifstream inputFile("less_memory/DNA", std::ios::binary);

    // if (!inputFile) {
    //     std::cerr << "Failed to open the file." << std::endl;
    //     return T;
    // }

    int NORM_WINDOW_SIZE = std::ceil(WINDOW_SIZE  * 3 / BYTE_SIZE) + 1;
    int byte_num = 0;
    int cur_pos_in_byte = 0;
    char buffer[NORM_WINDOW_SIZE];

    inputFile.seekg(start);
    
    inputFile.read(buffer, NORM_WINDOW_SIZE);

    cur_pos_in_byte = start_in_byte;

    unsigned char bitmask = 0x01; // Битовая маска

    vector<int> T = vector<int>(WINDOW_SIZE, 0);
    vector<int> C = vector<int>(WINDOW_SIZE, 0);
    vector<int> A = vector<int>(WINDOW_SIZE, 0);
    vector<int> G = vector<int>(WINDOW_SIZE, 0);

    for (int i = 0; i < WINDOW_SIZE; i++) {
        int f = get_next(cur_pos_in_byte, byte_num);
        int first_bit = (buffer[byte_num] & (1 << (7 - f))) != 0;
        int s = get_next(cur_pos_in_byte, byte_num);
        int second_bit = (buffer[byte_num] & (1 << (7 - s))) != 0;
        int t = get_next(cur_pos_in_byte, byte_num);
        int third_bit = (buffer[byte_num] & (1 << (7 - t))) != 0;

        if (first_bit == 0 && second_bit == 0 && third_bit == 1){
            T[i] = 1;
        } else if (first_bit == 1 && second_bit == 0 && third_bit == 0){
            A[i] = 1;
        } else if (first_bit == 0 && second_bit == 1 && third_bit == 1){
            G[i] = 1;
        } else if (first_bit == 0 && second_bit == 1 && third_bit == 0){
            C[i] = 1;
        } 
        // std::cout << first_bit << " " << second_bit << " " << third_bit << "\n";
    }

    return T;
}

vector<int> get_lines(int chr, int start, int WINDOW_SIZE) {
    // assert(start + WINDOW_SIZE <= (df.loc[chr].byte_count * 8 - df.loc[chr].waste_bits) / 3, "Make the starting position smaller or choose a different chromosome");
    return get_one_hot(metadata[chr].start + std::ceil(start * 3.0 / BYTE_SIZE), start * 3 % BYTE_SIZE, WINDOW_SIZE);
}

void get_time() {
  std::vector<double> times;
  std::vector<int> sizes;
  
  for (int i = 1; i < 11; i++) {
    int WINDOW_SIZE = 100000 * i;
    std::cout << "Window size: " << WINDOW_SIZE << endl;
    int NORM_WINDOW_SIZE = std::ceil(WINDOW_SIZE * 3.0 / BYTE_SIZE);
    
    std::clock_t start_time = std::clock();
    for (int j = 0; j < 1000; j++) {
      int chr = 0;
      int start_pos = std::rand() % 2000000;
      std::vector<int> result = get_lines(chr, start_pos, WINDOW_SIZE);
    }
    
    double res_time = (std::clock() - start_time) / (double)CLOCKS_PER_SEC;
    times.push_back(res_time);
    sizes.push_back(WINDOW_SIZE);
    std::cout << "--- " << res_time << " seconds ---" << std::endl;
  }
}

std::vector<Data> read_csv(const std::string& filename) {
    std::ifstream file(filename);

    if (file.is_open()) {
        std::string line;
        std::getline(file, line); // Пропускаем заголовок

        while (std::getline(file, line)) {
            std::istringstream iss(line);
            std::string start_str, byte_count_str, waste_bits_str;
            std::getline(iss, start_str, ',');
            std::getline(iss, byte_count_str, ',');
            std::getline(iss, waste_bits_str, ',');

            int start = std::stoi(start_str);
            int byte_count = std::stoi(byte_count_str);
            int waste_bits = std::stoi(waste_bits_str);

            Data d = {start, byte_count, waste_bits};
            metadata.push_back(d);
        }

        file.close();
    }

    return metadata;
}


int main() {    
    read_csv("less_memory/metadata.csv");

    // get_lines(1, 0);
    get_time();
}