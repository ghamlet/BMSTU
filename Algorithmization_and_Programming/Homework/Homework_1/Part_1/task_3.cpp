#include <iostream>
#include <cmath>
#include <iomanip>

using namespace std;

int main() {
    long double x;
    cout << "Введите значение x (в радианах): ";
    cin >> x;

    long double sin2x = pow(sin(x), 2);
    long double cos2x = pow(cos(x), 2); 
    long double result = sin2x + cos2x; 

    cout << fixed << setprecision(16);
    cout << "x: " << x << endl;
    cout << "sin^2(x) = " << setw(20) << sin2x << endl;
    cout << "cos^2(x) = " << setw(20) << cos2x << endl;
    cout << "sin^2(x) + cos^2(x) = " << setw(20) << result << endl;

    // Оценка погрешности
    long double delta = fabs(result - 1);
    cout << "Погрешность = " << setw(20) << delta << endl;
}


