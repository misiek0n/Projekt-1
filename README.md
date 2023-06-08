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

- neu (przelicza współrzędne geocentryczne odbiornika do współrzędnych topocentrycznych n, e, u na podstawie współrzędnych x,y,z odbiornika i satelitów)

W przypadku gdy użytkownik wprowadzi niepoprawną nazwę elipsoidy program wykona przeliczenie dla elipsoidy GRS80.

Przykładowe formaty plików txt wraz z opisem kolejnych kolumn dla poszczególnych funckji:
- flh2xyz:
	- Współrzędna Fi punktu wyrażona w stopniach
	- Współrzędna Lambda punktu wyrażona w stopniach
	- Współrzędna h punktu wyrażona w metrach		

	Przykładowy plik ze współrzędnymi:
	
		48.99962126;23.29857641;170.776
		49.10032645;22.87394074;256.009

- xyz2flh:
	- Współrzędna X punktu wyrażona w metrach
	- Współrzędna Y punktu wyrażona w metrach
	- Współrzędna Z punktu wyrażona w metrach		

	Przykładowy plik ze współrzędnymi:
	
		3850700.000;1658260.000;4790660.000
		3855141.595;1626409.701;4798064.775
		
- pl2000:
	- Współrzędna Fi punktu wyrażona w stopniach
	- Współrzędna Lambda punktu wyrażona w stopniach
	- Południk osiowy strefy odwzorowawczej wyrażony w stopniach		

	Przykładowy plik ze współrzędnymi:
	
		48.99962126;23.29857641;24
		49.10033002;22.87392559;24
	
- pl1992:
	- Współrzędna Fi punktu wyrażona w stopniach
	- Współrzędna Lambda punktu wyrażona w stopniach
	- Południk osiowy strefy odwzorowawczej wyrażony w stopniach		

	Przykładowy plik ze współrzędnymi:
	
		48.99962126;23.29857641;19
		49.10033002;22.87392559;19
		
- neu: 
	- Współrzędna X odbiornika wyrażona w metrach
	- Współrzędna Y odbiornika wyrażona w metrach
	- Współrzędna Z odbiornika wyrażona w metrach
	- Współrzędna X odbiornika wyrażona w metrach
	- Współrzędna Y odbiornika wyrażona w metrach
	- Współrzędna Z odbiornika wyrażona w metrach  		

	Przykładowy plik ze współrzędnymi:
	
		3850699.999412209;1658259.999949739;4790659.999869207;3855141.5954925404;1626409.7007365027;4798064.7745897975

Przykładowe wywołania fukcji wraz z przykładowym wyglądem pliku wynikowego współrzędnych po transformacji:

-flh2xyz:

			python -m proj1 -md grs80 -f flh2xyz -p wsp_flh2xyz.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach oddzielonych spacjami znajdują się:
	- Współrzędna X punktu wyrażona w metrach,
	- Współrzędna Y punktu wyrażona w metrach,
	- Współrzędna Z punktu wyrażona w metrach
	
		3850699.999412209 1658259.999949739 4790659.999869207
		3855141.5954925404 1626409.7007365027 4798064.7745897975

		
- xyz2flh:

			python -m proj1 -md grs80 -f xyz2flh -p wsp_xyz2flh.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna Fi punktu wyrażona w stopniach,
	- Współrzędna Lambda punktu wyrażona w stopniach,
	- Współrzędna h punktu wyrażona w metrach
	
		48.99962125697281 23.29857640745372 170.77647551055998
		49.10032645480258 22.873940745946097 256.00909447763115


-pl2000:

			python -m proj1 -md grs80 -f pl2000 -p wsp_pl2000.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna X punktu w układzie 2000 wyrażona w metrach,
	- Współrzędna Y punktu w układzie 2000 wyrażona w metrach
	
		5429404.521804485 8448679.317698374
		5440977.237802496 8417775.823952498

		

-pl1992

			python -m proj1 -md grs80 -f pl1992 -p wsp_pl1992.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna X punktu w układzie 1992 wyrażona w metrach,
	- Współrzędna Y punktu w układzie 1992 wyrażona w metrach
	
		134689.95555297006 814275.8236125545
		144204.8400629703 782663.6525562805

		
	
-neu

			python -m proj1 -md grs80 -f neu -p wsp_neu.txt
				
Wygląd pliku ze współrzędnymi po transformacji, gdzie w kolejnych kolumnach znajdują się:
	- Współrzędna N punktu wyrażona w metrach,
	- Współrzędna E punktu wyrażona w metrach,
	- Współrzędna U punktu wyrażona w metrach
	
		>30453.541142497546 12580.170679525723 1822.405534565127
		

3. Znane błędy, które nie zostały naprawione

TRANSFORMACJA KRASOWSKI -> PL2000 ORAZ KRASOWSKI -> PL1992 NIE POWINNA BYĆ UŻYWANA ZE WZGLĘDU NA NIEPOPRAWNE WYNIKI OBLICZEŃ!!!

W przypadku gdy mimo zalecenia nie używania tej tranformacji użytkownik spróbuje ją wywołać program zwróci wiadomość:

		Transformacja KRASOWSKI -> PL2000/PL1992 nie działa poprawnie. Pomijam wykonanie obliczeń.
