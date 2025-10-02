#include "../../include/animals/Animal.h"

int Animal::id_count = 0;

Animal::Animal(int x, int y, int d, int s) : x(x), y(y), direction(d), stability(s), age(0), is_alive(true) {
    id = id_count;
    id_count++;
};


Animal::~Animal() = default;

int Animal::get_id() {
    return id;
}

int Animal::get_birth_step() {
    return birth_step;
}

void Animal::set_x(int value) {
    x = value;
}

void Animal::set_y(int value) {
    y = value;
}

int Animal::get_x() {
    return x;
}

int Animal::get_y() {
    return y;
}

int Animal::get_direction() {
    return direction;
}

int Animal::get_age() {
    return age;
}

int Animal::get_stability() {
    return stability;
}

void Animal::aging() {
    age++;
}

void Animal::die() {
    is_alive = false;
}

bool Animal::alive() {
    return is_alive;
}

void Animal::change_direction() {
    switch (direction)
    {
    case constants::SOUTH:
        direction = constants::EAST;
        break;
    case constants::EAST:
        direction = constants::NORTH;
        break;
    case constants::NORTH:
        direction = constants::WEST;
        break;
    case constants::WEST:
        direction = constants::SOUTH;
        break;
    default:
        break;
    }
}

