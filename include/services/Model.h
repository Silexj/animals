#ifndef MODEL_H
#define MODEL_H
#include <vector>
#include "Fox.h"
#include "Rabbit.h"

class Model {
private:
    int **grid;
    int grid_n;
    int grid_m;
    std::vector<Fox> foxes;
    std::vector<Rabbit> rabbits;

    void move_fox(Fox fox) {

    }

    void move_rabbit(Rabbit rabbit) {
        
    }
};

#endif