using uint64 = unsigned long long;

class Uint2048 {
 public:
  Uint2048();
  Uint2048(const int &x);

  bool operator<(const Uint2048 &other) const;
  bool operator==(const Uint2048 &other) const;
  Uint2048 operator+(const Uint2048 &other) const;
  Uint2048 operator-(const Uint2048 &other) const;
  Uint2048 operator*(const Uint2048 &other) const;
  Uint2048 operator/(const Uint2048 divisor) const;

  void Print() const;
  static int NumAdditions();
  // Ne peut pas être const, puisqu'en tant que static elle ne peut que
  // accéder aux attributs statiques.

 private:
  uint64 u_[32];
  static int number_of_additions;
  
  bool BitAt(int i) const;
  static Uint2048 TwoToThePower(int i);
  int MostSignificantBit() const;
};
