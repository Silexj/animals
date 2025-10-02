#include "../../include/animals/Fox.h"


Fox::Fox(int x, int y, int d, int s) : Animal(x, y, d, s), hunger(2), age_parent(0) {};

Fox::Fox(int x, int y, int d, int s, int age_parent, int step): Animal(x, y, d, s), hunger(2), age_parent(age_parent) {
    birth_step = step;
};

int Fox::get_age_parent() {
    return age_parent;
}

void Fox::set_hunger(int h) {
    hunger = h;
}

int Fox::get_hunger() {
    return hunger;
}

void Fox::movement(int height, int width, int step) {
    switch (direction) {
        case constants::NORTH:
            if (y + constants::MOVE_FOX >= height) {
                y = (y + constants::MOVE_FOX) - height;
            } else {
                y = (y + constants::MOVE_FOX);
            }
            break;
        case constants::EAST:
            if (x + constants::MOVE_FOX >= width) {
                x = ((x + constants::MOVE_FOX) - width);
            } else {
                x = x + constants::MOVE_FOX;
            }
            break;
        case constants::SOUTH:
            if (y - constants::MOVE_FOX < 0) {
                y = (height + (y - constants::MOVE_FOX));
            } else {
                y = (y - constants::MOVE_FOX);
            }
            break;
        case constants::WEST:
            if (x - constants::MOVE_FOX < 0) {
                x = (width + (x - constants::MOVE_FOX));
            } else {
                x = (x - constants::MOVE_FOX);
            }
            break;
    }
    if (step % stability == 0) {
        change_direction();
    }
}

Animal* Fox::reproduce(int step) const {
    return new Fox(x, y, direction, stability, age_parent, step);
}

bool Fox::can_reproduce() const {
    return hunger < 1;
}