#ifndef MODEL_H
#define MODEL_H
#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include "../animals/Fox.h"
#include "../animals/Rabbit.h"
#include "../utils/Constants.h"

#include "../utils/json.hpp" // 

using json = nlohmann::json;

class Model {
private:
    int **grid;
    int grid_n;
    int grid_m;
    std::vector<Fox*> foxes;
    std::vector<Rabbit*> rabbits;
    int step;

    json simulation_history;
    void record_step_state();
public:

    Model(int n, int m);

    ~Model();

    void add_fox(int x, int y, int d, int s);
    void add_rabbit(int x, int y, int d, int s);

    void next_step();
    void dying();
    void reproduction();
    void feeding();
    void aging();
    void move();
    void print_step();
    
    void run_simulation(int steps);
    void export_to_json(const std::string& filename) const;
};

#endif