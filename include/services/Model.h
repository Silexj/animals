#ifndef MODEL_H
#define MODEL_H
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

    void add_fox(int x, int y, int d, int s);
    void add_rabbit(int x, int y, int d, int s);


    void dying();
    void reproduction();
    void feeding();
    void aging();
    void move();
    void print_step();
};

#endif