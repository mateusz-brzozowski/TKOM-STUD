# Temat projektu
Język do opisu figur geometrycznych i ich właściwości.Podstawowe typy figur geometrycznych (trójkąt, prostokąt, romb,trapez,koło itd.) są wbudowanymi typami języka. Każdy typ posiada wbudowane metody służące do wyznaczania charakterystycznych dla niego wielkości, np. obwód, pole powierzchni, wysokość, średnica itp.Kolekcja figur tworzy scenę wyświetlaną na ekranie.

Wariant: `Język statycznie typowany z silnym typowaniem`

Język programowania: `Python`

# przykłady wykorzystania języka

[//]: # (TODO: Bardziej złożone przykłady wykorzystania, skomplikowane wyrażenia)

- wyznaczanie pola figury
```c++
Triangle t = Triangle(3, 4, 55);
print(t.area());
```
- wyznaczanie obwodu figury
```c++
Rectangle r = Rectangle(5);
print(r.perimeter());
```
- wyznaczanie przekątnej figury
```c++
Square s = Square(5);
print(s.diagonal());
```
- dodawanie/usuwanie figur do/z kolekcji i wyświetlanie ich
[//]: # (TODO: punkt wywalić do figury)
```c++
Canvas c = Canvas();
Circle circle = Circle(6);
Polygon p = Polygon(5, 6);
Rhomb r = Rhomb(4, 60);
Trapeze t = Trapeze(6, 8, 60, 90);
c.push(circle, 0,0);
c.push(p, 10, 10);
c.push(r, 1, 10);
c.push(t, -5, 8);
c.pop();
c.display();
```
- przesuwanie figur o wektor
```c++
Circle shape = Circle(5)
shape.move(2,3)
```

# Opis funkcjonalności

Język do opisu figur geometrycznych i ich właściwości umożliwia opisanie i obliczanie charakterystycznych wielkości dla różnych typów figur geometrycznych.

Każdy typ figury geometrycznej jest reprezentowany przez swoje właściwości. Metody wbudowane umożliwiają wyznaczenie charakterystycznych dla danej figury wielkości. Wyniki obliczeń można wyświetlić na ekranie w formie tekstowej.

Kolekcja figur geometrycznych tworzy scenę, na której użytkownik może umieszczać figury i dokonywać na nich różnych operacji, takich jak skalowanie i przenoszenie

Figury geometryczne i ich charakterystyczne wielkości:

- Koło:
    - Promień (r) - odległość od środka koła do dowolnego punktu na jego obwodzie.
    - Średnica (d) - dwukrotność promienia.
- Kwadrat:
    - Bok (a) - długość każdej z czterech równych krawędzi.
    - Przekątna (diagonal) - odległość między dwoma przeciwległymi wierzchołkami.
    - Promień okręgu wpisanego (r) i promień okręgu opisanego (R)
- Prostokąt:
    - Bok krótszy (a) i bok dłuższy (b) - długości dwóch przeciwległych krawędzi.
    - Przekątna (d) - odległość między dwoma przeciwległymi wierzchołkami.
    - Promień okręgu opisanego (R)
- Trójkąt:
    - Bok (a), bok (b) i bok (c) - długości trzech krawędzi.
    - Wysokość (h) - pionowa odległość między jednym z wierzchołków a przeciwległą krawędzią.
    - Promień okręgu wpisanego (r) i promień okręgu opisanego (R)
- Romb:
    - Bok (a) - długość każdej z czterech równych krawędzi.
    - Przekątna (e) i przekątna (f) - długości dwóch przeciwległych przekątnych.
    - Kąt między przekątnymi (α) - kąt pomiędzy przekątnymi, mierzony w stopniach.
    - Promień okręgu wpisanego (r)
- Trapez:
    - Bok (c) i bok (d) - długości dwóch równoległych krawędzi.
    - Wysokość (h) - pionowa odległość między dwoma równoległymi krawędziami.
    - Podstawa mniejsza (a) i podstawa większa (b) - długości dwóch pozostałych krawędzi.
    - Kąt wewnętrzne przy podstawie (α) i (β)
    - Promień okręgu wpisanego (r) i promień okręgu opisanego (R)
- Wielokąt formeny:
    - Bok (a) - długość każdej z krawędzi.
    - Liczba boków (n) - liczba krawędzi w wielokącie.
    - Kąt wewnętrzny (α) - kąt pomiędzy dwoma sąsiednimi krawędziami
    - Promień okręgu wpisanego (r) i promień okręgu opisanego (R)

Metody dla wszystkich figur:

- Pole powierzchni (area)
- Obwód (perimeter)
- Przesuń o wektor (move)

Kolekcja figur służąca do wyświetlania:

- Płótno (canvas)
    - dodawanie elementu do kolekcji (push)
    - usuwanie ostatnio dodanego elementu z kolekcji (pop)
    - wyświetlanie kolekcji (display)

# Wymagania funkcjonalne i niefunkcjonalne

[//]: # (TODO: Pomieszane wymagania z założeniami, dodać wymagania niefunkcjonalne)

1. Typowanie statyczne, silne typowanie, Mutowalność
2. Każda instrukcja musi być zakończona znakiem `;`
3. Program musi zawierać funkcję `main()`, która jest funkcją startową
4. Program składa się z bloków funkcji, które zawarte są między znakami `{`, `}`
5. Funkcję mogę być wywoływane rekursywnie
6. Zmienne widoczne są jedynie w blokach, poza nimi już nie
7. Rzutowanie wartości liczbowych, ucięcie cyfr po przecinku
8. W wywołaniach funkcji typy, przekazujemy przez referencję
9. Typy danych:
- proste
    - `int` - typ liczby całkowita,
    - `dec` - typ zmienno przecinkowy (liczba dziesiętna - decimal)
    - `bool` - wartość logiczna (prawda/fałsz)
- złożone
    - `String` - ciąg znaków
    [//]: # (TODO: dodać shape)
    - `Circle(value)` - koło
        - jako argumenty podajemy promień koła, promień może być typu int lub float z wartością dodatnią.
    - `Square(value)` - kwadrat
        - jako argumenty podajemy bok kwadratu, bok może być typu int lub float z wartością dodatnią.
    - `Rectangle(value, value)` - prostokąt
        - jako argumenty podajemy boki kwadratu, boki mogą być typu int lub float z wartością dodatnią
    - `Triangle(value, value, value)` - trójkąt
        - jako argumenty podajemy dwa boki trójkąta i kąt pomiędzy nimi, boki mogą być typu int lub float z wartością dodatnią, natomiast kąt jest typu int z zakresu od 0 do 180.
    - `Rhomb(value, value, value)` - romb
        - jako argumenty podajemy bok rombu i kąt pomiędzy nimi, bok może być typu int lub float z wartością dodatnią, natomiast kąt jest typu int z zakresu od 0 do 180.
    - `Trapeze(value, value, value, value)` - trapez
        - jako argumenty podajemy dwie podstawy trapezu i kąty przy dłuższej podstawie, boki mogą być typu int lub float z wartością dodatnią, natomiast kąty są typu int z zakresu od 0 do 90.
    - `Polygon(value, value)` - wielokąt foremny
        - jako argumenty podajemy bok i ilość boków, bok może być typu int lub float z wartością dodatnią, natomiast ilość boków może być typu int o wartości co najmniej 3.
    - `Canvas` - kolekcja figur
        - do kolekcji możemy dodawać figury `push(shape)`
        - usuwanie elementu z kolekcji `pop()`
        - wyświetlanie kolekcji `display()`
7. operatory arytmetyczne:
- `+` - dodawanie
- `-` - odejmowanie
- `*` - mnożenie
- `/` - dzielenie
8. operatory logiczne:
- `and` - koniunkcja
- `or` - alternatywa
- `not` - negacja
9. operatory porównania:
- `>` - większy
- `>=` - większy równy
- `<` - mniejszy
- `<=` - mniejszy równy
- `==` - równy
- `!=` - nierówny
9. instrukcja warunkowa:
- `if`:
```c++
if (warunek){

} else if (warunek){

} else {

};
```
10. pętle
- `while` - pętla warunkowe
```c++
while (warunek) {

};
```
- `for` - pętla iterująca po elementach kolekcji

```c++
Canvas canvas = Canvas();
for ( Shape shape : canvas){

};
```
11. Funkcje. Jeżeli funkcja zwraca wartość musi rozpoczynać się od typu, który zwraca, natomiast, jeżeli funkcja nic nie zwraca musi on zaczynać się od słowa `def`
```c++
def Rectangle nazwa( int a, dec b){
    Circle circle = Circle(a);
    print(circle.area());
    return Rectangle(a, b);
};

def nazwa(Rectangle r){
    print(r.area());
};
```
12. Komentarze, umożliwiamy komentarze w jednej linii
```python
# to jest komentarz
```
13. Deklaracja zmiennych, umożliwiamy przypisywanie nowej wartości do zmiennych
```c++
bool isSquare = False;
bool isCircle = True;
bool isRect = isSquare;
isCircle = isRect;
```

# Tokeny

```py
ADD :  "+",
SUBTRACT : "-",
MULTIPLY : "*",
DIVIDE : "/",

AND : "and",
OR : "or",
NOT : "not",

EQUAL : "==",
NOT_EQUAL : "!=",
GREATER : ">",
LESS : "<",
GREATER_EQUAL : ">=",
LESS_EQUAL : "<=",

COMMENT : "#",

INTEGER : "int",
DECIMAL : "dec",
BOOL : "bool",

BOOL_TRUE : "True",
BOOL_FALSE : "False",

String : "String",

STRING_QUOTE : "\"",
STRING_QUOTE : "\`",

Shape : "Shape",
Circle : "Circle",
Square : "Square",
Rectangle : "Rectangle",
Triangle : "Triangle",
Rhomb : "Rhomb",
Trapeze : "Trapeze",
Polygon : "Polygon",
Canvas : "Canvas",

SEMICOLON : ";",
COLON : ":",
COMMA : ",",
DOT : ".",

FUNCTION : "def",
RETURN : "return",

START_CURLY : "{",
STOP_CURLY : "}",
START_ROUND : "(",
STOP_ROUND : ")",
START_SQUARE : "[",
STOP_SQUARE : "]",

IF : "if",
ELSE : "else",

WHILE : "while",
FOR : "for",
```

# Gramatyka
[//]: # (TODO: zrobić XD, Priorytet operatorów, typowe błędy: konwersja między typami , operator "-" uważać, że to jeden z najniższych operatorów)

```py
lowercase_letter    = 'a' | 'b' | ... | 'z'
uppercase_letter    = 'A' | 'B' | ... | 'Z'
not_zero_digit      = '1' | '2' | ... | '9'
zero                = '0'
digit               = zero | not_zero_digit
subtract_operator   = "+" | "-"
multiply_operator   = "*" | "/"

IF                  = "if", '(', LOGICAL_CONDITION, ')', STATEMENT, [ "else", STATEMENT]

STATEMENT           = IF | WHILE | FOR |
```

# Obsługa błędów:

- Napotkanie błędu powoduje wyświetlenie odpowiedniego komunikatu użytkownikowi.

Komunikat składa się z numera wiersza lini oraz numera kolumny w którym dany błąd wystąpił, następnie wyświetlana jest treść komunikatu

[//]: # (TODO: podać różne rodzaje błędów jakie będę obsługiwał np. składniowe, semantyczne wymienić kategorie jakie będą obsługiwane i przykłady Expected ';' ponieważ oczekiwano tego i tametego bo tu)

```cpp
def main(){
    int a = 1
    Circle
}
```
```c++
Error [2, 14]: Expected ';'
```

# Sposób Uruchomiania

Program można uruchomiać za pomocą programu napisanego w języku python podając odpowiednie do argumenty przy jego wywołaniu.

Do poprawnego działania wymagany jest zainstalowany `Python` w wersji `3.9.0`, a także zainstalowane wymagane biblioteki znajdujące się w pliku `requirements.txt`.

Sposób instalacji: `pip3 install -r requirements.txt`.

Przykładowy sposób uruchomienia:

```bash
$ ./run.py code.txt
```


[//]: # (TODO: jak wygląda wynik)

# Testowanie

Projekt zawiera testy jednostkowe oraz testy integracyjne, sprawdzające poprawność działającego kodu jak i programu.

Wykorzystywana biblioteka: `pytest`

[//]: # (TODO: Przykłady testów i te negatywne)

# Biblioteki

[//]: # (TODO: z jakich bibliotek będę korzystał)



[//]: # (TODO: wykorzystywane struktury danych ????)
