#include <iostream>
using namespace std;


bool allDigitsOdd(int number)
{
    int units = number % 10;    // единицы
    int tens = (number / 10) % 10; // десятки
    int hundreds = number / 100;   // сотни

    // Проверяем, что все цифры нечетные
    if (units % 2 != 0 && tens % 2 != 0 && hundreds % 2 != 0)
    {
        return true;
    }
}


int main(){

    for (int num=111; num <=999; num++)
    {
       if (allDigitsOdd(num))
       cout << num << endl;
    }
    return 0;
}