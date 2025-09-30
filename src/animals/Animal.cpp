#include "Animal.h"
#include "Constants.h"

Animal::Animal(int x, int y, int d, int s) : x(x), y(y), direction(d), stability(s), age(0) {};


Animal::~Animal() = default;

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

