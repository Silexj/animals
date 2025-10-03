#include "../../include/services/Model.h"

Model::Model(int n, int m): grid_n(n), grid_m(m), step(0) {
    grid = new int*[n];
    for (int i = 0; i < n; i++) {
        grid[i] = new int[m]{0};
    }
}

Model::~Model() {
    for (int i = 0; i < grid_n; i++) {
        delete[] grid[i];
    }
    delete[] grid;

    for (auto f : foxes) {
        delete f;
    }
    for (auto r : rabbits) {
        delete r;
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
    std::cout << "======================STEP " << step << "======================" << std::endl;
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
            grid[new_fox->get_y()][new_fox->get_x()]--;
            foxes.push_back(new_fox);
        } else if (Rabbit* new_rabbit = dynamic_cast<Rabbit*>(nb)) {
            grid[new_rabbit->get_y()][new_fox->get_x()]++;
            rabbits.push_back(new_rabbit);
        }
    }
}

void Model::dying() {
    for (auto it = foxes.begin(); it != foxes.end(); ) {
        if ((*it)->get_age() == constants::MAX_AGE_FOX) {
            grid[(*it)->get_y()][(*it)->get_x()]++;
            delete *it;
            it = foxes.erase(it);
        } else {
            ++it;
        }
    }

    for (auto it = rabbits.begin(); it != rabbits.end(); ) {
        if (!(*it)->alive() || (*it)->get_age() >= constants::MAX_AGE_RABBIT) {
            grid[(*it)->get_y()][(*it)->get_x()]--;
            delete *it;
            it = rabbits.erase(it);
        } else {
            ++it;
        }
    }
}

void Model::next_step() {
    move();
    feeding();
    aging();
    reproduction();
    dying();

    print_step();
}

void Model::print_game(int steps) {
    // if (steps != 0) {
    //     std::cout << "Game not valid!" << std::endl;
    //     return;
    // } 
    print_step();
    for (int i = 0; i < steps; i++) {
        next_step();
        print_step();
    }
}

void Model::write_step() {
    std::ofstream out_file("output.txt");

    if (!out_file.is_open()) {
        std::cerr << "File not open!" << std::endl;
        return;
    }
    std::cout << "======================STEP " << step << "======================" << std::endl;
    for (int i = 0; i < grid_n; i++) {
        for (int j = 0; j < grid_m; j++) {
            if (grid[i][j] == 0) {
                out_file << "*\t";
            } else {
                out_file << grid[i][j] << "\t";
            }
        }
        out_file << std::endl;
    }
    out_file.close();
}