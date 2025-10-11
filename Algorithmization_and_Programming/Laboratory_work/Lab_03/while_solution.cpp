#include <iostream>
using namespace std;

bool allDigitsOdd(int number)
{
    int units = number % 10;                                       // единицы
    int tens = (number / 10) % 10;                                 // десятки
    int hundreds = number / 100;                                   // сотни
    return (units % 2 != 0 && tens % 2 != 0 && hundreds % 2 != 0); // Проверяем, что все цифры нечетные
}

int main()
{
    int num = 111;
    int count = 0;

    while (num <= 999)
    {
        if (allDigitsOdd(num))
            { cout << num << endl;
              count++;
            }
        num++;
    }
    cout << count << endl;
    return 0;
}

