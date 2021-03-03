#include <iostream>
#include <vector>
#include "2048_arithmetic.h"

// En utilisant le passage par référence on prend 3x moins de temps au test.

using namespace std;

Uint2048::Uint2048() {
    for (int i=0; i<32; i++) {
        u_[i] = 0;
    }
}

Uint2048::Uint2048(const int &x) {
    u_[0] = x;
    for (int i=1; i<32; i++) {
        u_[i] = 0;
    }
}
bool Uint2048::operator<(const Uint2048 &other) const{
    for (int i=31; i>=0; i--) {
        if (u_[i] < other.u_[i]) {
            return true;
        }
        else if (u_[i] != other.u_[i]) {
            return false;
        }
    }
    return false;
}

bool Uint2048::operator==(const Uint2048 &other) const {
    for (int i=0; i<32; i++) {
        if (u_[i] != other.u_[i]) {return false;}
    }
    return true;
}

Uint2048 Uint2048::operator+(const Uint2048 &other) const{
  number_of_additions++;

  Uint2048 result;
  uint64 carry = 0;
  for (int i = 0; i < 32; ++i) {
    result.u_[i] = u_[i] + other.u_[i] + carry;
    // Detect overflows, which indicate that there should be a carry.
    // It's not that simple!
    if ((carry == 0 && result.u_[i] < u_[i]) ||
        (carry == 1 && result.u_[i] <= other.u_[i])) {
      carry = 1;
    } else {
      carry = 0;
    }
  }
  // The last carry is lost.
  return result;
}

Uint2048 Uint2048::operator-(const Uint2048 &other) const{
    Uint2048 result;
    bool carry, next_carry;
    carry = 0;
    
    for (int i=0; i<32; i++) {
        next_carry = 0;
        if (u_[i] < (other.u_[i]+carry) || (other.u_[i]+carry == 0 && carry == 1)) {
            next_carry = 1;
        }
        result.u_[i] = u_[i] - other.u_[i] - carry;
        carry = next_carry;
    }
    return result;
}

Uint2048 Uint2048::operator*(const Uint2048 &x) const {
    const Uint2048 zero(0);
    Uint2048 y = *this;
    Uint2048 r(0);

    for (int i=0; i<2048; i++) {
        if (x.BitAt(i)) {
            r = r + y;
        }
        y = y+y;
    }
    return r;
}

Uint2048 Uint2048::operator/(const Uint2048 divisor) const {
    Uint2048 result(0);
    const Uint2048 zero(0); // pour faire des comparaisons
    if (*this < divisor) {return result;}

    int i = this->MostSignificantBit() - divisor.MostSignificantBit();
    // i est le plus grand i tel que 2^j * divisor < *this

    Uint2048 candidate;
    while (i >= 0) {
        Uint2048 two_to_the_i = TwoToThePower(i); // 
        candidate = divisor*(result + two_to_the_i);

        if (candidate < *this) {
            result = result + two_to_the_i;

        }
        else if (candidate == *this) {
            result = result + two_to_the_i;
            return result;
        }
        i--;
    }
    return result;

}

void Uint2048::Print() const{
  // The difficulty is to print the number in base 10.
  // First, precompute *all* the powers of 10 that are smaller or equal to x.
  // Since 2^2048 ~= 10^616.5, we need up to 617 powers: 10^0...10^616.
  int p = 0;
  Uint2048 cur(1);  // 10^p
  Uint2048 p10[617];  // p10[i] will be equal to 10^i.
  p10[0] = cur;
  while (p < 616 && !(*this < cur)) {
    // Simple way of computing p10 * 10 with few additions.
    Uint2048 tmp2 = cur + cur;
    Uint2048 tmp4 = tmp2 + tmp2;
    Uint2048 tmp8 = tmp4 + tmp4;
    cur = tmp8 + tmp2;
    p++;
    p10[p] = cur;
  }

  // Now, compute the digits in base 10, one by ones.
  Uint2048 s(0);
  if (p > 0) --p;
  while (p >= 0) { 
    int d;  // Declared outside the "for" loop to keep its value after it's done
    for (d = 0; d < 10; ++d) {
      Uint2048 t = s + p10[p];
      if (*this < t) break;
      s = t;
    }
    cout << d;
    p--;
  }
}

int Uint2048::number_of_additions = 0;

int Uint2048::NumAdditions() {
    return number_of_additions;
}

// --- Private methods below ---

bool Uint2048::BitAt(int i) const {
    // Returns the bit at position i (0 being the least-significant one).
    return (u_[i/64] & (1ul << (i % 64)));
}

Uint2048 Uint2048::TwoToThePower(int i) {
    Uint2048 result(0);
    result.u_[i/64] = (1ul << (i % 64));
    return result;
}

int Uint2048::MostSignificantBit() const {
    for (int i=2047; i>=0; i--) {
        if (this->BitAt(i)) {return i;}
    }
    return 0;
}
