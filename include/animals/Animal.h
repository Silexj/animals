#ifndef ANIMAL_H
#define ANIMAL_H
#include "../utils/Constants.h"


class Animal {
private:
    static int id_count;
    int id;
protected:
    int x;
    int y;
    int direction;
    int stability;
    int age;
    int birth_step;
    bool is_alive;

public:
    Animal(int x, int y, int d, int s);

    virtual ~Animal();

    int get_id();
    int get_birth_step();

    void set_x(int value);
    void set_y(int value);
    int get_x();
    int get_y();
    int get_direction();
    int get_age();
    int get_stability();
    bool alive();

    

    virtual Animal* reproduce(int step) const = 0;
    virtual bool can_reproduce() const = 0;
    virtual void movement(int height, int width, int step) = 0;
    void change_direction();
    void aging();
    void die();

};

#endif