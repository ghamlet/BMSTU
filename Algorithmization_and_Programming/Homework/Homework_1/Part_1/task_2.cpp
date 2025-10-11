#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main() {
    long double x;
    cout << "Enter x: ";
    cin >> x;

    long double y1 = (exp(x) - exp(-x)) / 2;
    long double y2 = (exp(x) + exp(-x)) / 2;
    long double y = pow(y2, 2) - pow(y1, 2);

    cout << setprecision(18);
    cout << "x: " << x << endl;
    cout << "y1 (sh(x)) = " << setw(22) << y1 << endl;
    cout << "y2 (ch(x)) = " << setw(22) << y2 << endl;
    cout << "y (y2^2 - y1^2) = " << setw(22) << y << endl;
    cout << "Абсолютная погрешность: " << setw(22) << fabs(1 - y) << endl;
    cout << "Относительная погрешность: " << setw(22) << fabs(1 - y) / 1 << endl;
}
