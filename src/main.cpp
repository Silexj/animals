#include "../include/services/Model.h"

int main() {
    Model m = Model(3, 3);
    m.add_fox(0, 1, 0, 2);
    m.print_step();
}