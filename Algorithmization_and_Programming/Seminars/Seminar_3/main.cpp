#include <iostream>
#include <cmath>

int main()
{
    double S, R, x, eps; // ввод через экспоненциальную запись работает
    int i =0;

    puts("Ведите x eps: \n");
    scanf("%lf %lf", &x, &eps);  

    printf("%20.10lf\n%20.10lf\n", x, eps); // умеет округлять

    R = pow(10,10);

    while (fabs(R) > eps ) 
    {
        i++; // получаем номер текущего элемента
        R = ((pow(x, i+i-1)) / (i+i-1)) * (pow(-1, i+1));
        S = S+R;
        printf("S= %20.16lf\n", S);
    }

    printf("ArcTg = %30.16lf\n", atan(x));
    printf("Result=%30.16lf\n", S);

    return 0;
}