#include <iostream>
#include <cmath>

using namespace std;

int main()
{
    double x, result;
    const double pi = 3.141592653589793;

    cout << "Введите x: " << endl;
    cin >> x;

    if (x<0) result = 0;
    else if (0 <= x < 1.5) result = pow((sin(x) +cos(x)), 2);
    else result = sin(x) - sqrt(x + cos(pi * x *x));

    cout << "Значение функции= " << result << endl;
    return 0;
}

