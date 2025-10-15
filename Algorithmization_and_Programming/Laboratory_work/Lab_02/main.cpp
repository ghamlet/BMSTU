#include <iostream>
#include <fstream>
#include <string>
using namespace std;

// Функция для отображения ASCII-арта
void displayAsciiArt() {
    ifstream file("graph-ascii-art.txt");
    string line;
    
    if (file.is_open()) {
        while (getline(file, line)) {
            cout << line << endl;
        }
        file.close();
    } else {
        cout << "Не удалось открыть файл" << endl;
    }
}


int main(){

    displayAsciiArt();

    double x, y;
    cout << "Введите x и y \n";
    cin >> x >> y;

    if (y < -2*x*x +1)  // лежит ли точка внутри параболы
    {
        if (y < x)  // лежит ли точка под прямой y=x
        {
            if ((y > 0) && (x > 0)) // лежит ли точка в I четверти
                cout << "Точка лежит в заштрихованной области \n";
            
            else cout << "Точка НЕ лежит в заштрихованной области \n";   
        } 
        else cout << "Точка НЕ лежит в заштрихованной области \n";   
    } 
    else cout << "Точка НЕ лежит в заштрихованной области \n"; 

    return 0;
}

