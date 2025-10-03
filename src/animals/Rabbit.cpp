#include "../../include/animals/Rabbit.h"

Rabbit::Rabbit(int x, int y, int d, int s): Animal(x, y, d, s) {};

Rabbit::Rabbit(int x, int y, int d, int s, int step): Animal(x, y, d, s){
    birth_step = step;
};

Rabbit::Rabbit(): Animal() {};


void Rabbit::movement(int height, int width, int step) {
    switch (direction) {
        case constants::SOUTH:
            if (y + constants::MOVE_RABBIT >= height) {
                // y = ((y + constants::MOVE_RABBIT) - height);
                y = 0;
            } else {
                y = (y + constants::MOVE_RABBIT);
            }
            break;
        case constants::EAST:
            if (x + constants::MOVE_RABBIT >= width) {
                // x = ((x + constants::MOVE_RABBIT) - width);
                x = 0;
            } else {
                x = (x + constants::MOVE_RABBIT);
            }
            break;
        case constants::NORTH:
            if (y - constants::MOVE_RABBIT < 0) {
                // y = (height + (y - constants::MOVE_RABBIT));
                y = height - 1;
            } else {
                y = (y - constants::MOVE_RABBIT);
            }
            break;
        case constants::WEST:
            if (x - constants::MOVE_RABBIT < 0) {
                // x = (width + (x - constants::MOVE_RABBIT));
                x = width - 1;
            } else {
                x = (x - constants::MOVE_RABBIT);
            }
            break;
    }
    if (step % stability == 0) {
        change_direction();
    }
}

Animal* Rabbit::reproduce(int step) const {
    return new Rabbit(x, y, direction, stability, step);
}

bool Rabbit::can_reproduce() const {
    return (age == 5 || age == 10) && is_alive;
}