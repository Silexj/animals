#ifndef FOX_H
#define FOX_H
#include "Animal.h"

class Fox: public Animal {
private:
    int hunger;

public: 
    Fox(int x, int y, int d, int s);
    void move() override;
    void aging() override; // ????
    void reproduction() const override;
    void eat();
};

#endif