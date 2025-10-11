#include <iostream>
using namespace std;



bool check_out_circle(float x, float y)
{
    if ((x *x + y*y ) > 4) 
    {
        printf("Точка находится вне круга \n");
        return true;
    } else {
        printf("Точка находится в кругу \n");
        return false;
    }
}


bool check_below_diagonal(float x, float y)
{
    if (y < x) 
    {
        printf("Точка находится под прямой y = x \n");

        return true; 
    }   else {
        printf("Точка находится над прямой y = x \n");

        return false;
    }
}


bool check_left_pos_vertikal(float x, float y)
{
    if (x < 2)
    {
        printf("Точка находится левее прямой x =2 \n");
        return true;

    } else {
        printf("Точка находится правее прямой x =2 \n");
        return false;
    }
}


bool check_over_x0(float x, float y)
{
    if (y > 0)
    {
        printf("Точка нходится выше прямой x0 \n");
        return true;

    }  else {
        printf("Точка нходится ниже прямой x0 \n");
        return false;
    }
}



int main()
{
    float x, y;
    bool was_stop_message = false;
    char choice;

    while ( !was_stop_message)
    {

    printf("Введите x и y: \n");
    int res = scanf("%f %f", &x, &y);

    
    printf("%f %f %c", x, y, '\n');

    // Проверяем условия
    bool below_diagonal = check_below_diagonal(x, y);
    bool left_vertical = check_left_pos_vertikal(x, y);
    bool out_circle = check_out_circle(x, y);
    bool over_x0 = check_over_x0(x, y);

    // Проверяем все условия
    if (below_diagonal && left_vertical && out_circle && over_x0)
    {
        printf("Точка принадлежит заданной области\n");
    }
    else
    {
        printf("Точка НЕ принадлежит заданной области\n");
    }


    printf("Хотите ввести значения еще раз?  y/n \n");
    scanf(" %c", &choice);

    if (choice == 'n')
        was_stop_message = true;
    


   }
}