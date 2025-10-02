#include "../../include/services/Model.h"

Model::Model(int n, int m): grid_n(n), grid_m(m){
    grid = new int*[n];
    for (int i = 0; i < n; i++) {
        grid[i] = new int[m]{0};
    }
}

void Model::add_fox(int x, int y, int d, int s) {
    foxes.push_back(new Fox(x, y, d, s));
    grid[y][x]--;
}

void Model::add_rabbit(int x, int y, int d, int s) {
    rabbits.push_back(new Rabbit(x, y, d, s));
    grid[y][x]++;
}

void Model::move() {
    step++;
    for (auto &f : foxes) {
        grid[f->get_y()][f->get_x()]++;
        f->movement(grid_n, grid_m, step);
        grid[f->get_y()][f->get_x()]--;
    }
    for (auto &r : rabbits) {
        grid[r->get_y()][r->get_x()]--;
        r->movement(grid_n, grid_m, step);
        grid[r->get_y()][r->get_x()]++;
    }
}

void Model::aging() {
    for (auto &f : foxes) {
        f->aging();
    }
    for (auto &r : rabbits) {
        r->aging();
    }
}

void Model::print_step() {
    for (int i = 0; i < grid_n; i++) {
        for (int j = 0; j < grid_m; j++) {
            if (grid[i][j] == 0) {
                std::cout << "*\t"; 
            } else {
                std::cout << grid[i][j] << "\t";
            }
        }
        std::cout << std::endl;
    }
}

void Model::feeding() {
    for (auto &r : rabbits) {
        std::vector<Fox*> dangers;
        for (auto &f : foxes) {
            if (r->get_x() == f->get_x() && r->get_y() == f->get_y()) {
                dangers.push_back(f);
            }
        }
        if (dangers.size() == 0) {
            continue;
        }
        Fox *chosen_fox = dangers[0];
        for (size_t i = 1; i < dangers.size(); i++) {
            if (chosen_fox->get_birth_step() > dangers[i]->get_birth_step()) {
                chosen_fox = dangers[i];
            } else if (chosen_fox->get_birth_step() == dangers[i]->get_birth_step()) {
                if (dangers[i]->get_birth_step() == 0) {
                    if (chosen_fox->get_id() > dangers[i]->get_id()) {
                        chosen_fox = dangers[i];
                    }
                } else {
                    if (chosen_fox->get_age_parent() < dangers[i]->get_age_parent()) {
                        chosen_fox = dangers[i];
                    }
                }
            }
        }
        chosen_fox->set_hunger(chosen_fox->get_hunger() - 1);
        grid[r->get_y()][r->get_x()]--;
        r->die();
    }
}

void Model::reproduction() {
    std::vector<Animal*> newborns;
    for (auto &f : foxes) {
        if (f->can_reproduce()) {
            Animal* child = f->reproduce(step);
            if (child != nullptr) {
                newborns.push_back(child);
            }
        }
    }
    for (auto &r : rabbits) {
        if (r->can_reproduce()) {
            Animal* child = r->reproduce(step);
            if (child != nullptr) {
                newborns.push_back(child);
            }
        }
    }
    for (auto &nb : newborns) {
        if (Fox* new_fox = dynamic_cast<Fox*>(nb)) {
            foxes.push_back(new_fox);
        } else if (Rabbit* new_rabbit = dynamic_cast<Rabbit*>(nb)) {
            rabbits.push_back(new_rabbit);
        }
    }
}

void Model::dying() {
    for (auto it = foxes.begin(); it != foxes.end(); ) {
        if ((*it)->get_age() == constants::MAX_AGE_FOX) {
            delete *it;
            it = foxes.erase(it);
        } else {
            ++it;
        }
    }

    for (auto it = rabbits.begin(); it != rabbits.end(); ) {
        if (!(*it)->alive() && (*it)->get_age() == constants::MAX_AGE_RABBIT) {
            delete *it;
            it = rabbits.erase(it);
        } else {
            ++it;
        }
    }
}