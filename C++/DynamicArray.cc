#include "DynamicArray.h"
#include <algorithm> // for max()
#include <iostream>

Array::Array(): size_(0) {
    capacity_ = initial_capacity;
    data_ = new double[capacity_];
}

Array::Array(const Array& original) {
    capacity_ = original.capacity_;
    size_ = original.size_;
    data_ = new double[capacity_]; // nouveau tableau

    for (int i=0; i<capacity_; i++) { // copies des valeurs
        data_[i] = original.data_[i];
    }
}

Array& Array::operator=(const Array& other) {
    size_ = other.size_;
    for (int i=0; i<size_; i++) { // copie des valeurs
        data_[i] = other.data_[i];
    }
    return *this;
}

Array::~Array() {
    delete[] data_;
}

int Array::size() const {
    return size_;
}

double& Array::operator[](int i) {
    return data_[i];
}

void Array::push_back(double x) {
    if (size_ > capacity_) {
        reallocate(capacity_multiplicator);
    }

    data_[size_] = x;
    size_++;
}

void Array::pop_back() {
    if (size_ == 0) {return;}

    if (size_ < capacity_ * freeing_multiplicator && size_ > initial_capacity) {
        reallocate(freeing_multiplicator);
    }

    size_--;
}

// --- Static attributes ---

double Array::capacity_multiplicator = 2;
double Array::freeing_multiplicator = .5;
int Array::initial_capacity= 10;

// --- Private methods ----

void Array::reallocate(double multiplicator) {
    capacity_ = std::max(int(capacity_ * multiplicator)+ 1, initial_capacity);

    double* new_data = new double[capacity_];
    //std::cout << size_ << "/" << capacity_ << std::endl;
    for (int i=0; i<size_; i++) {
        new_data[i] = data_[i];
    }
    delete[] data_;      // l'ancien tableau est effacé
    data_ = new_data;   // data_ pointe sur le nouveau tableau
}
