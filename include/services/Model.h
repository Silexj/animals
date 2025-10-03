#ifndef MODEL_H
#define MODEL_H
#include <fstream>
#include <string>
#include <vector>
#include <iostream>
#include "../animals/Fox.h"
#include "../animals/Rabbit.h"
#include "../utils/Constants.h"

class Model {
private:
    int **grid;
    int grid_n;
    int grid_m;
    std::vector<Fox*> foxes;
    std::vector<Rabbit*> rabbits;
    int step;
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
    void print_game(int steps);
    void write_step();
};

#endif