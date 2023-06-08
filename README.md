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

Przykładowe formaty plików txt wraz z opisem kolejnych kolumn dla poszczególnych funckji:
- flh2xyz:
	- Współrzędna Fi punktu wyrażona w stopniach
	- Współrzędna Lambda punktu wyrażona w stopniach
	- Współrzędna h punktu wyrażona w metrach		

	Przykładowy plik ze współrzędnymi:
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432

- xyz2flh:
	- Współrzędna X punktu wyrażona w metrach
	- Współrzędna Y punktu wyrażona w metrach
	- Współrzędna Z punktu wyrażona w metrach		

	Przykładowy plik ze współrzędnymi:
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
		
- pl2000:
	- Współrzędna Fi punktu wyrażona w stopniach
	- Współrzędna Lambda punktu wyrażona w stopniach
	- Numer strefy w której znajduje się punkt		

	Przykładowy plik ze współrzędnymi:
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
	
- pl1992:
	- Współrzędna Fi punktu wyrażona w stopniach
	- Współrzędna Lambda punktu wyrażona w stopniach		

	Przykładowy plik ze współrzędnymi:
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
		
- neu: 
	- Współrzędna X punktu A wyrażona w metrach
	- Współrzędna Y punktu A wyrażona w metrach
	- Współrzędna Z punktu A wyrażona w metrach
	- Współrzędna X punktu B wyrażona w metrach
	- Współrzędna Y punktu B wyrażona w metrach
	- Współrzędna Z punktu B wyrażona w metrach  		

	Przykładowy plik ze współrzędnymi:
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432

W celu wywołania programu konieczne jest uruchomienie wiersza poleceń w lokalizacji, w której znajduje się program.

Wywoływanie funkcji:

W celu wywołania funkcji należy użyć komendy:

		python -m proj1 -md nazwaelipsoidy -f nazwafunkcji -p nazwapliku.txt
		

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

W przypadku gdy użytkownik wprowadzi niepoprawną nazwę elipsoidy program wykona przeliczenie dla elipsoidy GRS80

Przykładowe wywołania fukcji wraz z przykładowym wyglądem pliku wynikowego współrzędnych po transformacji:

-flh2xyz:

			python -m proj1 -md grs80 -f flh2xyz -p wsp.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna X punktu wyrażona w metrach,
	- Współrzędna Y punktu wyrażona w metrach,
	- Współrzędna Z punktu wyrażona w metrach
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
		
- xyz2flh:

			python -m proj1 -md grs80 -f xyz2flh -p wsp.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna Fi punktu wyrażona w stopniach,
	- Współrzędna Lambda punktu wyrażona w stopniach,
	- Współrzędna h punktu wyrażona w metrach
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432

-pl2000:

			python -m proj1 -md grs80 -f pl2000 -p wsp.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna X punktu w układzie 2000 wyrażona w metrach,
	- Współrzędna Y punktu w układzie 2000 wyrażona w metrach
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
		

-pl1992

			python -m proj1 -md grs80 -f pl2000 -p wsp.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna X punktu w układzie 1992 wyrażona w metrach,
	- Współrzędna Y punktu w układzie 1992 wyrażona w metrach
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
		
	
-neu

			python -m proj1 -md grs80 -f neu -p wsp.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna N punktu wyrażona w metrach,
	- Współrzędna E punktu wyrażona w metrach,
	- Współrzędna U punktu wyrażona w metrach
	
		>123.13;456.45;567.67  
		>100.10;431.432;432.432
		

3. Znane błędy, które nie zostały naprawione

W przypadku gdy użytkownik wprowadzi nazwe funkcji która nie jest obsługiwana, otrzyma błąd:

		proj1.py: error: argument fun: invalid choice: 'neu1' (choose from 'flh2xyz', 'xyz2flh', 'pl2000', 'pl1992', 'neu')

