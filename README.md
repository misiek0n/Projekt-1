TRANSFORMER jest programem służącym do transformacji współrzędnych między układami na elipsoidach odniesienia.
Program umożliwia przeliczenie współrzędnych w układach: FLH->XYZ, XYZ->FLH, FL->PL1992, FL->PL2000, FL->NEU.
Obecnie program obsługuje 3 elipsoidy odniesienia: GRS80, WGS84 oraz elipsoide Krasowskiego.

Program korzysta z :
-python w wersji 3.11 
-bibliotek:
	-numpy
	-math
	-argparse 
	
Obsługiwane systemy:
-Windows

Do działania programu konieczne jest utworzenie pliku ze współrzędnymi z rozszerzeniem txt.
W pliku ze współrzędnymi muszą znajdować się współrzędne oddzielone spacją, każdy kolejny punkt musi znajdować się w nowym wierszu.
W celu wywołania programu konieczne jest uruchomienie wiersza poleceń w lokalizacji, w której znajduje się program.

Wywoływanie funkcji:
W celu wywołania funkcji należy użyć komendy:

python -m proj1 nazwaelipsoidy nazwafunkcji nazwapliku.txt

Nazwy obsługiwanych elipsoid:
-grs80
-wgs84
-krasowski

Nazwy obsługiwanych funkcji:
-flh2xyz (przelicza współrzędne Fi, Lambda, H na współrzędne X, Y, Z)
-xyz2flh (przelicza współrzędne X, Y, Z na współrzędne Fi, Lambda, H)
-pl1992 (przelicza współrzędne Fi, Lambda do układu PL1992)
-pl2000 (przelicza współrzędne Fi, Lambda do układu PL2000)
-neu (przelicza współrzędne Fi, Lambda do układu NEU)

Znane błędy:
W przypadku, gdy w pliku ze współrzędnymi na końcu znajduje się więcej niż jedna pusta linia program wyrzuci błąd zamiany zmiennej typu string na float.

