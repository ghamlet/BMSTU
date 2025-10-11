#include <cmath>
#include <iostream>
using namespace std;

int main()
{
    long double eps, y;
    int n = 1;

    cout << "Введите эпсилон" << endl;
    cin >> eps;

    y = 2*eps;

    while (y > eps)
    {
        y = (n + 10) / (double)(n*n*n); // без double происходило бы целочисленное деление
        n++;
    }
    
    cout << "первый член последовательности которогый <= eps: " << y << endl;
    cout << "Количество итераций: " << n - 1 << endl; 
}


