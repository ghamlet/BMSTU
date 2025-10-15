# Массивы, строки и структуры. Адресная арифметика

## Содержание
- [3.1 Массивы](#31-массивы)
- [3.2 Адресация оперативной памяти](#32-адресация-оперативной-памяти)
- [3.3 Указатели](#33-указатели)
- [3.4 Управление динамической памятью](#34-управление-динамической-памятью)
- [3.5 Цикл foreach](#35-цикл-foreach)
- [3.6 Строки](#36-строки)
- [3.7 Структуры](#37-структуры)
- [3.8 Объединения](#38-объединения)

---

## 3.1 Массивы

### Определение массива
Массив - упорядоченная совокупность однотипных данных. Каждому элементу соответствует один или несколько индексов порядкового типа.

### Синтаксис объявления
```cpp
Тип Имя[Размер] {[Размер]} [[=] {Список_значений}];
```

**Характеристики:**
- **Тип** - любой кроме файла (может быть массивом, строкой и т.п.)
- **Размер** - натуральное значение, определяющее количество элементов
- **Максимальный размер** - не более 2 Гб в памяти
- **Размерность** - количество измерений

### Примеры объявлений
```cpp
int a[5];                          // одномерный массив
signed char с[3][3];               // двумерный массив
typedef signed char byte;          // объявление типа
byte c[3][3];                      // объявление матрицы
unsigned char b[256];              // объявление массива
```

### Инициализация
```cpp
int a[5] = {0,-3,7,3,5};
float d[3][5] = {{0.0,-3.6,7.8,3.789,5.0},
                 {6.1,0,-4.56,8.9,3.0},
                 {-0.35,-6.3,1.4,-2.8,1.9}};
```

### Типы массивов

#### Статические массивы
- Объявлены вне подпрограмм (`extern`) или как `static`
- Память выделяется во время компиляции

```cpp
float a[10][10];
int main() {
    int n,m;
    cout << "Enter n,m:";
    cin >> n >> m;
```

#### Автоматические массивы
- Локально объявлены внутри подпрограммы
- Память выделяется в стеке во время выполнения
- В Qt Creator (Clang) допускается указание размера переменными

```cpp
int main() {
    int n,m;
    cout << "Enter n,m:";
    cin >> n >> m;
    float a[n][m];  // Локальный массив с переменным размером
```

### Операции над массивами

#### Доступ к элементам
```cpp
int c[3][4];
c[2][0] = 5;        // прямой доступ

i = 2; j = 0;
c[i][j] = 5;        // косвенный доступ
```

#### Косвенный доступ для последовательной обработки
```cpp
for(i=0; i<6; i++) a[i] = i*i;
for(i=5; i>=0; i--) a[i] = i*i;
```

### Ввод-вывод массивов

#### Пример 1: Одномерный массив (C-style)
```cpp
int a[5];
for(i=0; i<5; i++) scanf("%d", &a[i]);
// или
for(i=0; i<5; i++) cin >> a[i];
```

**Формат ввода:** значения через пробел, Tab или Enter

#### Пример 2: Матрица (C-style)
```cpp
#include <stdio.h>
int main() {
    double a[10][10];
    int n,m,i,j;
    printf("Enter n,m:");
    scanf("%d %d", &n, &m);
    for(i=0; i<n; i++)
        for(j=0; j<m; j++)
            scanf("%lf", &a[i][j]);
    for(int i=0; i<n; i++) {
        for(int j=0; j<m; j++)
            printf("%5.2lf ", a[i][j]);
        printf("\n");
    }
    return 0;
}
```

#### Пример 3: Матрица (C++-style)
```cpp
#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    float a[10][10];
    int n,m,i,j;
    cout << "Enter n,m:";
    cin >> n >> m;
    for(i=0; i<n; i++)
        for(j=0; j<m; j++)
            cin >> a[i][j];
    cout << "Result:" << endl;
    for(int i=0; i<n; i++) {
        for(int j=0; j<m; j++)
            cout << setw(5) << a[i][j] << ' ';
        cout << "\n";
    }
    return 0;
}
```

### Поиск максимального элемента
```cpp
#include <stdio.h>
int main() {
    float a[5], amax; 
    int imax;
    puts("Enter 5 values:");
    for(int i=0; i<5; i++)
        scanf("%f", &a[i]);
    amax = a[0];
    imax = 0;
    for(int i=1; i<5; i++)
        if(a[i] > amax) {
            amax = a[i];
            imax = i;
        }
    puts("Values:");
    for(int i=0; i<5; i++)
        printf("%7.2f ", a[i]);
    printf("\n");
    printf("Max = %7.2f number = %5d\n", amax, imax+1);
    return 0;
}
```

### Алгоритмы поиска элемента

#### Неструктурный вариант (с досрочным выходом)
```cpp
#include <iostream>
using namespace std;
int a[10000];
int main() {
    int n,c,i;
    cout << "Enter n: "; cin >> n;
    cout << "Enter array:\n";
    for(int i=0; i<n; i++) cin >> a[i];
    cout << "Enter c: "; cin >> c;
    bool key = false;
    for(i=0; i<n; i++)
        if(a[i] == c) {
            key = true; 
            break;
        }
    if(key) cout << i << "Yes.\n";
    else cout << "No.\n";
    return 0;
}
```

#### Структурный вариант (с двумя условиями)
```cpp
#include <iostream>
using namespace std;
int a[10000];
int main() {
    int n,c;
    cout << "Enter n: "; cin >> n;
    cout << "Enter array:\n";
    for(int i=0; i<n; i++) cin >> a[i];
    cout << "Enter c: "; cin >> c;
    bool key = false; 
    int i = 0;
    while(i < n && !key)
        if(a[i] == c) key = !key;
        else i++;
    if(key) cout << i << "Yes.\n";
    else cout << "No.\n";
    return 0;
}
```

### Сумма элементов строк матрицы
```cpp
#include <iostream>
using namespace std;
int main() {
    float a[10][10], b[10];
    int n,m,i,j;
    cout << "Enter n,m:";
    cin >> n >> m;
    for(i=0; i<n; i++)
        for(j=0; j<m; j++)
            cin >> a[i][j];
    cout << "Result:" << endl;
    for(i=0; i<n; i++) {
        for(j=0, b[i]=0; j<m; j++) {
            cout << a[i][j] << ' ';
            b[i] += a[i][j];
        }
        cout << "Sum = " << b[i] << endl;
    }
    return 0;
}
```

---

## 3.2 Адресация оперативной памяти

### Основные понятия
- **Минимальная адресуемая единица** - байт
- **Байты памяти нумеруются** с нуля (номер = адрес)
- **Адрес программного объекта** - адрес его первого (младшего) байта
- **Объем занимаемой памяти** - количество байтов

### Проблемы распределения памяти
1. **Фрагментация памяти** - суммарный свободный объем достаточен, но непрерывного куска нужного размера нет
2. **Затраты на таблицы описаний** - часть памяти занята таблицей свободных/занятых блоков
3. **Неполные блоки** - неэффективное использование памяти

---

## 3.3 Указатели

### Определение
Указатель - тип данных для хранения адресов. Занимает 4 байта в 32-разрядных приложениях.

### Синтаксис объявления
```cpp
[Изменяемость_значения] Тип [Изменяемость_адреса] *Имя [=Адрес];
```

### Примеры объявлений
```cpp
short a, *ptrs = &a;           // обычный указатель
const short *ptrs;             // неизменяемое значение
short *const ptrs = &a;        // неизменяемый указатель
```

### Операции над указателями

#### 1. Присваивание
```cpp
int a, *ptri, *ptrj;
void *b;

ptri = &a;                     // адрес переменной
ptri = nullptr;                // нулевой адрес (C++11)
ptri = ptrj;                   // присваивание указателей
b = &a;                        // нетипизированный указатель
ptri = (int *)b;               // явное приведение (C-style)
ptri = static_cast<int*>(b);   // явное приведение (C++-style)
```

#### 2. Разыменование
```cpp
int c, a = 5, *ptri = &a;
void *b = &a;

c = *ptri;                     // чтение значения
*ptri = 125;                   // запись значения
*(int *)b = 6;                 // разыменование с приведением (C-style)
*static_cast<int*>(b) = 6;     // разыменование с приведением (C++-style)
```

### Основное правило адресной арифметики
```cpp
Указатель + n ⇔ Адрес + n * sizeof(Тип_данных)
```

**Примеры:**
```cpp
short a, *ptrs = &a;
ptrs++;                       // смещение на sizeof(short)
ptrs += 4;                    // смещение на 4 * sizeof(short)
*(ptrs + 2) = 2;              // доступ к элементу через смещение
```

### Ссылки
```cpp
int a,           // переменная
    *ptri = &a,  // указатель
    &b = a;      // ссылка (псевдоним)

a = 3;    ⇔    *ptri = 3;    ⇔    b = 3;
```

---

## 3.4 Управление динамической памятью

### A. C-style

#### Размещение одного значения
```cpp
int *a;
if ((a = (int *)malloc(sizeof(int))) == nullptr) {
    printf("Not enough memory.");
    exit(1);
}
*a = -244;
free(a);
```

#### Размещение нескольких значений
```cpp
int *list;
list = (int *)calloc(3, sizeof(int));
*list = -244;
*(list + 1) = 15;
*(list + 2) = -45;
free(list);
```

### B. C++-style

#### Размещение одного значения
```cpp
int *k;
k = new int;
*k = 85;

int *a;
if ((a = new int(-244)) == nullptr) {
    printf("Not enough memory.");
    exit(1);
}
delete a;
```

#### Размещение нескольких значений
```cpp
int *list;
list = new int[3];
*list = -244;
*(list + 1) = 15;
*(list + 2) = -45;
delete[] list;
```

### Организация массивов в C++
- Переменная массива - указатель на подряд идущие элементы
- Индексы всегда начинаются с 0
- Многомерные массивы расположены построчно
- Адресная арифметика: `(list+i) ⇔ &(list[i])` и `*(list+i) ⇔ list[i]`

### Варианты программы подсчета сумм строк

#### Автоматический массив (CLang)
```cpp
int a[n][n], s[n];  // память в стеке, освобождается автоматически
```

#### Динамический массив
```cpp
// Выделение памяти
int **a = new int*[n],
    *s = new int[n];
for(int i = 0; i < n; i++)
    a[i] = new int[n];

// Освобождение памяти
for(int i = 0; i < n; i++)
    delete[] a[i];
delete[] a;
delete[] s;
```

### Пример программы
```cpp
#include <iostream>
#include <iomanip>
using namespace std;
int main() {
    int n;
    cout << "Enter n:";
    cin >> n;
    int a[n][n], s[n];  // для компилятора CLang
    
    for(int i = 0; i < n; i++) {
        cout << "Enter numbers of " << i << " string:\n";
        for(int j = 0; j < n; j++) cin >> a[i][j];
    }
    
    for(int i = 0; i < n; i++) {
        s[i] = 0;
        for(int j = 0; j < n; j++) s[i] += a[i][j];
    }
    
    for(int i = 0; i < n; i++) {
        for(int j = 0; j < n; j++)
            cout << setw(3) << a[i][j];
        cout << " sum = " << s[i] << endl;
    }
    return 0;
}
```

### Многоуровневая адресация
```cpp
int m[] = {1,2,3,4};
int *mp[] = {m+3, m+2, m+1, m};

// Эквивалентные обращения:
mp[0], *mp
mp[1], *(mp+1)
mp[2], *(mp+2)
mp[3], *(mp+3)

m[1], *(m+1)
mp[0][-2], *(mp[0]-2), *(*mp-2)
mp[1][-1], *(mp[1]-1), *(*(mp+1)-1)
```

---

## 3.5 Цикл foreach

### Синтаксис
```cpp
for(тип &переменная : коллекция) { ... }  // для изменения
for(auto переменная : коллекция) { ... }   // работа с копиями
for(const auto &переменная : коллекция) { ... }  // доступ без изменений
```

### Пример
```cpp
#include <iostream>
using namespace std;
int main() {
    int arr[5] = {1, 2, 3, 4, 5};
    
    for(int &x : arr) {        // ссылка - для изменения
        x *= 2;
    }
    
    for(auto x : arr)          // значение - работа с копиями
        cout << x << ' ';
    
    for(const auto &x : arr)   // константа - запрет изменений
        cout << x << ' ';
    
    return 0;
}
```

**Примечание:** Размер массива должен быть известен!

---

## 3.6 Строки

### Определение
Строка в C/C++ - последовательность символов, завершающаяся нулевым байтом (`\0`).

**Примечание:** Цикл `foreach` для строк использовать нельзя, так как он не видит завершающего нуля.

### Объявление строк

#### С выделением памяти
```cpp
char Имя_указателя[Объем_памяти] [= Значение];
```

#### Указатель на строку
```cpp
char *Имя_указателя [= Значение];
```

### Примеры объявлений
```cpp
char str[6];                            // массив символов
char *ptrstr; ptrstr = new char[6];     // динамическая строка
char str1[5] = {'A','B','C','D','\0'}; // с инициализацией
char str2[5] = "ABCD";                  // строковая константа
char str3[] = "ABCD";                   // автоматическое определение размера
const char *str4 = "ABCD";              // константная строка
```

### Объявление массивов строк

#### Массив указателей на строки
```cpp
char *Имя[Размер] [= Значения];
```

#### Массив строк указанной длины
```cpp
char Имя[Размер][Размер] [= Значения];
```

### Примеры
```cpp
const char *mn[4] = {"One","Two","Three","Four"};  // массив указателей
char ms[4][7] = {"One","Two","Three","Four"};      // массив строк
```

### Ввод-вывод строк

#### Ввод
```cpp
char str[50];
gets(str);                    // устаревшая (до Enter)
gets_s(str,50);               // для VS
fgets(str,50,stdin);          // для Clang
scanf("%s",str);              // до пробела
cin >> str;                   // с использованием потока
```

#### Вывод
```cpp
puts(str);                    // вывод с переходом на новую строку
printf("String = %s\n",str);  // форматированный вывод
cout << str << endl;          // с использованием потока
```

### Функции работы со строками

#### 1. Определение длины строки
```cpp
size_t strlen(char *s);
```
```cpp
int k = strlen(str);
```

#### 2. Конкатенация (слияние) строк
```cpp
char *strcat(char *dest, const char *src);
```
```cpp
puts(strcat(s1,s2));    // или
strcat(s1,s2);          // результат в s1
```

#### 3. Сравнение строк
```cpp
int strcmp(const char *s1, const char *s2);
```
```cpp
k = strcmp(s1,s2);
// k=0 - строки равны, k>0 - первая больше, k<0 - вторая больше
```

#### 4. Копирование строки
```cpp
char *strcpy(char *dest, const char *src);
```
```cpp
puts(strcpy(s1,s2));    // или
strcpy(s1,s2);          // результат в s1
```

#### 5. Копирование фрагмента
```cpp
char *strncpy(char *dest, const char *src, size_t maxlen);
```
```cpp
strncpy(s1,"abcdef",3);  // копирует 3 символа
```

#### 6. Поиск символа в строке
```cpp
char *strchr(const char *s, int c);
```
```cpp
char *c1 = strchr(s,ch);  // возвращает адрес или nullptr
```

#### 7. Поиск подстроки
```cpp
char *strstr(const char *s1, const char *s2);
```
```cpp
char *c1 = strstr(s1,s2);  // возвращает адрес или nullptr
```

#### 8. Поиск токенов в строке
```cpp
char *strtok(char *strToken, const char *strDelimit);
```
```cpp
#include <string.h>
#include <stdio.h>
int main() {
    char str[] = "A string\tof,,tokens\nand some more tokens";
    char seps[] = " ,\t\n", *token;
    token = strtok(str, seps);
    while(token != nullptr) {
        printf("%s ", token);
        token = strtok(nullptr, seps);
    }
    return 0;
}
```

#### 9. Преобразование строки в целое число
```cpp
int atoi(const char *s);
```

#### 10. Преобразование строки в вещественное число
```cpp
double atof(const char *s);
```

#### 11. Преобразование числа в строку (MVS)
```cpp
char *itoa(int value, char *s, int radix);  // radix - основание СС
```

#### 12-13. Преобразование вещественного числа в строку (MVS)
```cpp
char *fcvt(double value, int decimals, int *dec, int *sign);
char *ecvt(double value, int count, int *dec, int *sign);
```

#### 14. Формирование строки по формату
```cpp
int sprintf(char *buf, const char *format, arg-list);
```
```cpp
char str[80];
sprintf(str, "%s %d %c", "one", 2, '3');
cout << str << endl;  // one 2 3
```

### Пример преобразования числа в строку
```cpp
#include <stdlib.h>
#include <stdio.h>
int main() {
    char *buf;
    int decimal, sign;
    int count = 10;
    
    buf = ecvt(3.1415926535, count, &decimal, &sign);
    printf("Converted value to string: %s\n", buf);
    printf("Decimal= %d, Sign= %d.", decimal, sign);
    return 0;
}
// Output: Converted value to string: 31415926535
//         Decimal= 1, Sign= 0.
```

### Удаление лишних пробелов из строки
```cpp
#include <string.h>
#include <stdio.h>
int main() {
    char st[40];
    puts("Enter string");
    fgets(st, sizeof(st), stdin);  // вместо gets(st)
    
    int n = strlen(st);  // на последнем месте стоит \n
    st[n-1] = '\0';
    
    while(char *p = strstr(st,"  "))
        strcpy(p, p+1);
        
    if(st[0] == ' ')
        strcpy(st, st+1);
        
    if(int k = strlen(st)) {
        if(st[k-1] == ' ')
            st[k-1] = '\0';
        printf("R = %s.\n", st);
    }
    else puts("Empty string.");
    return 0;
}
```

### Преобразование последовательности строк
**Формат:** "Иванов Иван Иванович 1956" → "Иванов И.И. 67"

```cpp
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
int main() {
    char st[80], stres[80], strab[80], *c1, *c2, *c3;
    int old;
    
    while((puts("Enter string or end:"),
           strcmp(gets(st), "end") != 0)) {
        strcpy(stres, st);
        c1 = strchr(stres, ' ');
        *(c1+2) = '.';
        
        c2 = strchr(st, ' ');
        c2 = strchr(c2+1, ' ');
        strncpy(c1+3, c2+1, 1);
        strncpy(c1+4, ". \0", 3);
        
        c3 = strchr(c2+1, ' ');
        old = 2023 - atoi(c3+1);
        
        sprintf(strab, "%d", old);  // itoa(old, strab, 10);
        strcat(stres, strab);
        puts(stres);
    }
    return 0;
}
```

---

## 3.7 Структуры

### Определение
Структура - последовательность полей различных типов.

### A. C-style объявление

#### С именем структуры
```cpp
struct [Имя_структуры] {
    {Описание_поля}
} [{Переменная [= Значение]}];

[struct] Имя_структуры {Переменная [= Значение]};
```

#### Без имени структуры
```cpp
struct {
    {Описание_поля}
} {Переменная [= Значение]};
```

### Примеры
```cpp
// С именем структуры
struct student {
    char name[22];
    char family[22];
    int old;
};
struct student stud1 = {"Petr", "Petrov", 19}, stud[10], *ptrstud;

// Без имени структуры
struct {
    char name[22];
    char family[22];
    int old;
} stud1, stud[10], *ptrstud;
```

### B. C++-style объявление
```cpp
typedef struct {
    {Описание_поля}
} Имя_структуры;

[struct] Имя_структуры {Переменная [= Значение]};
```

### Пример
```cpp
typedef struct {
    char name[22];
    char family[22];
    int old;
} student;

struct student stud1 = {"Petr", "Petrov", 19}, stud[10], *ptrstud;
```

### Обращение к полям структуры
```cpp
Имя_переменной.Имя_поля
Имя_массива[Индекс].Имя_поля
(*Имя_указателя).Имя_поля    ⇔    Имя_указателя->Имя_поля
```

### Примеры обращений
```cpp
stud1.name
stud[i].name
(*ptrstud).name    ⇔    ptrstud->name
```

### Пример: Массив записей
```cpp
#include <string.h>
#include <stdio.h>

struct data {                    // структура даты
    unsigned short year;         // год
    unsigned short month;        // месяц
    unsigned short day;          // день
};

struct record {                  // структура записи
    char fam[22];               // фамилия
    data birthday;              // день рождения
};

int main() {
    record basa[40];            // массив из 40 структур
    char name[22];              // строка для ввода фамилии
    bool key;                   // переменная для поиска
    int n;                      // количество записей
    
    // Ввод записей
    printf("Enter n:");
    scanf("%d", &n);
    for(int i=0; i<n; i++) {
        printf("Enter family: ");
        scanf("%s", basa[i].fam);
        printf("Enter birthday year: ");
        scanf("%hu", &basa[i].birthday.year);
        printf("Enter birthday month: ");
        scanf("%hu", &basa[i].birthday.month);
        printf("Enter birthday day: ");
        scanf("%hu", &basa[i].birthday.day);
    }
    
    // Вывод списка
    puts("List:");
    for(int i=0; i<n; i++) {
        printf("%s ", basa[i].fam);
        printf("%d.", basa[i].birthday.year);
        printf("%d.", basa[i].birthday.month);
        printf("%d\n", basa[i].birthday.day);
    }
    
    // Поиск по фамилии
    printf("Enter family: ");
    scanf("%s", name);
    
    key = false;
    int i = 0;
    while(i < n && !key)
        if(strcmp(basa[i].fam, name))
            i++;
        else key = true;
    
    // Вывод результата
    if(key) {
        printf("%s ", basa[i].fam);
        printf("%d.", basa[i].birthday.year);
        printf("%d.", basa[i].birthday.month);
        printf("%d\n", basa[i].birthday.day);
    }
    else puts("No data.");
    
    return 0;
}
```

### Пример: Средний балл студентов
```cpp
#include <stdio.h>
#include <string.h>

typedef struct {
    char name[10];
    int ball;
} test;

typedef struct {
    char family[22];
    test results[5];
} student;

int main() {
    student stud[10];
    int i, n = 0;
    float avarstud, avarage = 0;
    
    while(puts("Input names, subjects and marks or end"),
          scanf("\n%s", stud[n].family),
          strcmp(stud[n].family, "end") != 0) {
        for(avarstud = 0, i = 0; i < 3; i++) {
            scanf("\n%s %d", stud[n].results[i].name,
                  &stud[n].results[i].ball);
            avarstud += stud[n].results[i].ball;
        }
        printf("Average:%s=%5.2f\n", stud[n].family, avarstud/3);
        avarage += avarstud;
        n++;
    }
    printf("Group average mark=%5.2f\n", avarage/n/3);
    return 0;
}
```

---

## 3.8 Объединения

### Определение
Объединение - тип данных, позволяющий хранить разные типы данных в одной области памяти.

### Синтаксис
```cpp
union [Имя_объединения] {
    {Описание_поля}
} [{Переменная [= Значение]}];

[union] Имя_объединения {Переменная [= Значение]};
```

### Пример
```cpp
union mem {
    double d;
    long l;
    int k[2];
};
```

**Особенность:** Все поля объединения занимают одну и ту же область памяти. Размер объединения равен размеру наибольшего поля.
