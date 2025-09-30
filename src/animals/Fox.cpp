#include "Fox.h"
#include "Constants.h"

Fox::Fox(int x, int y, int d, int s) : Animal(x, y, d, s), hunger(2) {};

void Fox::aging() {
    age++;
    if (age > constants::MAX_AGE_FOX) {
        die();
    }
}

void Fox::move() {
    switch (direction)
    {
    case constants::SOUTH:
        
        break;
    
    default:
        break;
    }
}