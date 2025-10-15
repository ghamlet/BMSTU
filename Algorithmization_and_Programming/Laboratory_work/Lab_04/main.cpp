#include <iostream>
using namespace std;

int main()
{
    int n, count=0, sum = 0; 
    cout << "Введите n<=50" << endl;
    cin >> n;

    int arr[n];
    for (int i=0; i<n; i++){
        cin >> arr[i];
    }

    cout << "Исходный массив: " << endl;
    for (int i=0; i<n; i++){

        if (arr[i] < 0) count++;
        if (arr[i] % 3 ==0) sum+=arr[i];
        cout << arr[i] << " ";
    }

    cout << endl;
    cout << "Количество отрицательных элементов: " << count <<  endl;
    cout << "Сумма элементов кратных 3: " << sum <<  endl;
    return 0;
}