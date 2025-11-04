#ifndef RABBIT_H
#define RABBIT_H
#include "../../include/animals/Animal.h"
#include "../utils/Constants.h"


class Rabbit: public Animal {
public:
    Rabbit(int x, int y, int d, int s);
    Rabbit(int x, int y, int d, int s, int step);
    Rabbit();

    Animal* reproduce(int step) const override;
    bool can_reproduce() const override;
    void movement(int height, int width, int step) override;
};

#endif