#include <iostream>
#include <cmath>

using namespace std;


int main() {
    float y;
    cout << "До инициализации y = " << y << endl;
    
    y = 1;
    cout << "После инициализации y = " << y << endl;
    
    y = y / 6000;
    y = exp(y);
    y = sqrt(y);
    y = y / 14;
    
    y = 14 * y;
    y = y * y;
    y = log(y);
    y = 6000 * y;
    
    cout << "После преобразований y = " << y << endl;

    return 0;
}


