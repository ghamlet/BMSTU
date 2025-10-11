#include <stdio.h>
#include "Nod.h"


int main()
{

  int a,b;

  puts("Enter two integer values");
  scanf("%d %d", &a, &b);
  printf("Nod %d and %d = %d.\n", a, b, nod(a,b));

}
