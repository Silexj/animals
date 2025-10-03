#include "../include/services/Model.h"

int main() {
    std::ifstream config_file("input.txt");

    if (!config_file.is_open()) {
        std::cerr << "File not open!" << std::endl;
        return -1;
    }
    int n, m, steps;
    config_file >> m >> n >> steps;

    Model M = Model(n, m);
    int num_foxes, num_rabbits;
    config_file >> num_rabbits >> num_foxes;
    
    for (int i = 0; i < num_rabbits; ++i) {
        int x, y, d, s;
        config_file >> x >> y >> d >> s;
        M.add_rabbit(x, y, d, s);
    }
    for (int i = 0; i < num_foxes; ++i) {
        int x, y, d, s;
        config_file >> x >> y >> d >> s;
        M.add_fox(x, y, d, s);
    }

    M.print_game(steps);
    M.write_step();
}