#include <iostream>
using namespace std;

int main()
{
    int n, sum = 0;

    cout << "Введите натуральное число: ";
    cin >> n;

    if (n > 0)
    {
        for (int i = 1; i <= n / 2; i++)
        {
            if (n % i == 0)
            {
                sum += i;
            }
        }

        if (sum == n)
        {
            cout << n << " - совершенное число" << endl;
        }
        else
        {
            cout << n << " - не совершенное число" << endl;
        }
        
    }
     else {
        cout << "n должно быть натуральным" << endl;
     }

   

    return 0;
}