#ifndef FOX_H
#define FOX_H
#include "../../include/animals/Animal.h"
#include "../utils/Constants.h"

class Fox: public Animal {
private:
    int hunger;
    int age_parent;

public: 
    Fox(int x, int y, int d, int s);
    Fox(int x, int y, int d, int s, int age_parent, int step);

    int get_age_parent();
    int get_hunger();
    void set_hunger(int h);

    Animal* reproduce(int step) const override;
    bool can_reproduce() const override;
    void movement(int height, int width, int step) override;
};

#endif