#ifndef ANIMAL_H
#define ANIMAL_H

class Animal {
protected:
    int x;
    int y;
    int direction;
    int stability;
    int age;


public:
    Animal(int x, int y, int d, int s);

    virtual ~Animal();

    virtual void move() = 0;
    virtual void aging() = 0;
    virtual void reproduction() const = 0;
    virtual void die() = 0;
    void change_direction();
};

#endif