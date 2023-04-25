1.Opis działania programu:

TRANSFORMER jest programem służącym do transformacji współrzędnych między układami na elipsoidach odniesienia.
Program umożliwia przeliczenie współrzędnych w układach: FLH->XYZ, XYZ->FLH, FL->PL1992, FL->PL2000, FL->NEU.
Obecnie program obsługuje 3 elipsoidy odniesienia: GRS80, WGS84 oraz elipsoide Krasowskiego.

Program korzysta z :

- python w wersji 3.11 

- bibliotek:

	- numpy
	
	- math
	
	- argparse 
	
Obsługiwane systemy:

- Windows

2. Korzystanie z programu:

Do działania programu konieczne jest utworzenie pliku ze współrzędnymi z rozszerzeniem txt.
W pliku ze współrzędnymi muszą znajdować się współrzędne oddzielone średnikiem, każdy kolejny punkt musi znajdować się w nowym wierszu.

Przykładowy format pliku txt:

		123.13;456.45;567.67
		100.10;431.432;432.432

W celu wywołania programu konieczne jest uruchomienie wiersza poleceń w lokalizacji, w której znajduje się program.

Wywoływanie funkcji:

W celu wywołania funkcji należy użyć komendy:

		python -m proj1 nazwaelipsoidy nazwafunkcji nazwapliku.txt

Zamiast nazwy pliku użytkownik może też podać ścieżke do jego lokalizacji.

		python -m proj1 nazwaelipsoidy nazwafunkcji "sciezka_do_pliku"

Nazwy obsługiwanych elipsoid:

- GRS80

- WGS84

- Krasowski

Nazwy obsługiwanych funkcji:

- flh2xyz (przelicza współrzędne Fi, Lambda, H na współrzędne X, Y, Z)

- xyz2flh (przelicza współrzędne X, Y, Z na współrzędne Fi, Lambda, H)

- pl1992 (przelicza współrzędne Fi, Lambda do układu PL1992)

- pl2000 (przelicza współrzędne Fi, Lambda do układu PL2000)

- neu (przelicza współrzędne Fi, Lambda do układu NEU)

