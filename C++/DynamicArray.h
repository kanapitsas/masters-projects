// This class represents an array of doubles, with a fixed capacity
// determined at construction.
class Array {
 public:
  // The array will be empty at construction, but all the memory 
  // necessary to store up to "capacity" doubles will already be allocated.
  Array();
  Array(const Array& original);
  Array& operator=(const Array& other);

  // It is important to clean up the memory at destruction!
  ~Array();

  // Returns the current size (i.e. number of elements) of the array.
  int size() const;

  // Returns the *mutable* element at index #i.
  double& operator[](int i);

  // Adds an element at the last position of the array.
  void push_back(double x);

  // Removes the last element of the array.
  void pop_back();

  // Facteur par lequel sera multiplicée la nouvelle capacité du tableau,
  // une fois qu'on aura atteint sa limite.
  static double capacity_multiplicator;
  static double freeing_multiplicator;
  static int initial_capacity;

 private:
  // Alloue un nouveau tableau mémoire en multipliant la capacité par multiplicator,
  // sans jamais déscendre en dessous de initial_capacity.
  void reallocate(double multiplicator);

  int size_;
  int capacity_;
  double* data_;
};
