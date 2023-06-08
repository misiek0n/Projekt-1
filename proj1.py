import numpy as np
from math import *
import argparse


def dms(x):
    znak = ' '
    if x < 0:
        znak = '-'
        x = abs(x)
    x = x * 180/pi
    d = int(x)
    m = int((x - d) * 60)
    s = (x - d - m / 60) * 3600
    print(znak, "%3d°%2d'%7.5f\"" % (d, m, s))


class Transformer:
    def __init__(self, model):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy - promień równikowy
            b - mała półoś elipsoidy - promień południkowy
            Domyslna elipsoida: grs80
        """
        self.model = model
        if model == 'grs80':
            self.a = 6378137
            self.e2 = 0.00669438002290
        elif model == 'wgs84':
            self.a = 6378137
            self.e2 = 0.00669437999014
        elif model == 'krasowski':
            self.a = 6378245
            self.e2 = 0.00669342162296
        else:
            raise NotImplementedError(f"{model} nie ma takiego modelu :( ")

    def xyz2flh(self, x, y, z):
        """
        Algorytm Hirvonena - algorytm transformacji współrzędnych ortokartezjańskich (x, y, z)
        na współrzędne geodezyjne długość szerokość i wysokośc elipsoidalna (phi, lam, h). Jest to proces iteracyjny. 
        W wyniku 3-4-krotneej iteracji wyznaczenia wsp. phi można przeliczyć współrzędne z dokładnoscią ok 1 cm.     
        Parameters
        ----------
        x, y, z : FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        latfi
            [stopnie dziesiętne] - szerokość geodezyjna
        la
            [stopnie dziesiętne] - długośc geodezyjna.
        h : TYPE
            [metry] - wysokość elipsoidalna
        output [STR] - optional, defoulf 
            dec_degree - decimal degree
            dms - degree, minutes, sec
        """
        p = sqrt(x ** 2 + y ** 2)
        fi = np.arctan(z / (p * (1 - self.e2)))

        while True:
            n = self.a / np.sqrt(1 - self.e2 * sin(fi)**2)
            h = p / cos(fi) - n
            fp = fi
            fi = np.arctan(z / (p * (1 - self.e2 * n / (n + h))))
            if abs(fp - fi) < (0.000001 / 206265):
                break

        la = np.arctan2(y, x)
        print(f'Wynik transformacji XYZ -> BLH na elipsoidzie {self.model} to:\n')
        dms(fi)
        dms(la)
        print(f'{h:.3f}')
        return degrees(fi), degrees(la), h

    def flh2xyz(self, fi, la, h):

        """
        Algorytm transformacji współrzędnych geodezyjnych (phi, lam, h)
        na współrzędne kartezjańskie (phi, lam, h). Współrzędne obliczane są przez podstawienie parametrów wejciowych do wektora normalnego
        Parameters
        ----------
        fi, la, h : FLOAT
             współrzędne w układzie orto-kartezjańskim, 

        Returns
        -------
        x
            [metry] - wartosc na pierwszej osi
        y
            [metry] - wartosć na drugiej osi
        z : 
            [metry] - wartosć na trzeciej osi
        """
        fi = radians(fi)
        la = radians(la)
        n = self.a / np.sqrt(1 - self.e2 * sin(fi)**2)
        x = (n + h) * cos(fi) * cos(la)
        y = (n + h) * cos(fi) * sin(la)
        z = (n + h - n * self.e2) * sin(fi)
        print(f'Wynik transformacji BLH -> XYZ na elipsoidzie {self.model} to:\n'
              f'X = {x:.3f}\n'
              f'Y = {y:.3f}\n'
              f'Z = {z:.3f}')
        return x, y, z

    def pl1992(self, fi, lam, l0):
        """
        Algorytm transformacji współrzędnych geodezyjnych (fi, lam,)
        na współrzędne płaskie prostokątne (x, y) w ukladzie PL-1992. Współrzędne obliczane stosując odwzorowanie Gaussa-Krugera 
        w jednej 10stopniowej strefie o południku osiowym 19°E.
        skala m0 = 0.9993
        Parameters
        ----------
        fi, lam: FLOAT
             współrzędne geodezyjne, 

        Returns
        -------
        x
            [metry] - wartosc na pierwszej osi
        y
            [metry] - wartosć na drugiej osi
       
        """
        fi = radians(fi)
        lam = radians(lam)
        lam0 = radians(l0)
        m0 = 0.9993
        b2 = self.a ** 2 * (1 - self.e2)
        ep2 = (self.a ** 2 - b2) / b2
        dl = lam - lam0
        t = tan(fi)
        n2 = ep2 * cos(fi) ** 2
        n = self.a / np.sqrt(1 - self.e2 * sin(fi)**2)
        a0 = 1 - self.e2 / 4 - 3 * self.e2 ** 2 / 64 - 5 * self.e2 ** 3 / 256
        a2 = (3 / 8) * (self.e2 + self.e2 ** 2 / 4 + 15 * self.e2 ** 3 / 128)
        a4 = (15 / 256) * (self.e2 ** 2 + (3 * self.e2 ** 3) / 4)
        a6 = 35 * self.e2 ** 3 / 3072
        sigma = self.a * (a0 * fi - a2 * sin(2 * fi) + a4 * sin(4 * fi) - a6 * sin(6 * fi))
        xgk = sigma + (dl ** 2 / 2) * n * sin(fi) * cos(fi) * \
              (1 + (dl ** 2 / 12) * cos(fi) ** 2 * (5 - t ** 2 + 9 * n2 + 4 * n2 ** 2) + ((dl ** 4) / 360) * cos(fi)
               ** 4 * (61 - 58 * t ** 2 + t ** 4 + 270 * n2 - 330 * n2 * t ** 2))
        ygk = dl * n * cos(fi) * (1 + (dl ** 2 / 6) * cos(fi) ** 2 * (1 - t ** 2 + n2) + (dl ** 4 / 120) * cos(fi)
                                  ** 4 * (5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2))
        x92 = xgk * m0 - 5300000
        y92 = ygk * m0 + 500000
        print(f'Wynik transformacji BL -> XY do układu PL-1992 na elipsoidzie {self.model} to:\n'
              f'X = {x92:.3f}\n'
              f'Y = {y92:.3f}')
        return x92, y92

    def pl2000(self, fi, lam, l0):
        """
        Algorytm transformacji współrzędnych geodezyjnych (fi, lam,)
        na współrzędne płaskie prostokątne (x, y) w układzie PL-2000. Współrzędne obliczane stosując odwzorowanie Gaussa-Krugera 
        w czterech 3 stopniowych strefach o południkach osiowych 15°E, 18°E, 21°E i 24°E,oznaczone kolejno numerami: 5,6,7,8.
        skala m0 = 0.999923
        Parameters
        ----------
        fi, lam: FLOAT
             współrzędne geodezyjne, 
        ns: INT
             numer strefy,

        Returns
        -------
        x
            [metry] - wartosc na pierwszej osi
        y
            [metry] - wartosć na drugiej osi
       
        """
        ns = l0 / 3
        l0 = radians(l0)
        m0 = 0.999923
        fi = radians(fi)
        lam = radians(lam)
        b2 = self.a ** 2 * (1 - self.e2)
        ep2 = (self.a ** 2 - b2) / b2
        dl = lam - l0
        t = tan(fi)
        n2 = ep2 * cos(fi) ** 2
        n = self.a / np.sqrt(1 - self.e2 * sin(fi)**2)
        a0 = 1 - self.e2 / 4 - 3 * self.e2 ** 2 / 64 - 5 * self.e2 ** 3 / 256
        a2 = (3 / 8) * (self.e2 + self.e2 ** 2 / 4 + 15 * self.e2 ** 3 / 128)
        a4 = (15 / 256) * (self.e2 ** 2 + (3 * self.e2 ** 3) / 4)
        a6 = 35 * self.e2 ** 3 / 3072
        sigma = self.a * (a0 * fi - a2 * sin(2 * fi) + a4 * sin(4 * fi) - a6 * sin(6 * fi))
        xgk = sigma + (dl ** 2 / 2) * n * sin(fi) * cos(fi) * (
                    1 + (dl ** 2 / 12) * cos(fi) ** 2 * (5 - t ** 2 + 9 * n2 + 4 * n2 ** 2) + (
                        (dl ** 4) / 360) * cos(fi) ** 4 *
                    (61 - 58 * t ** 2 + t ** 4 + 270 * n2 - 330 * n2 * t ** 2))
        ygk = dl * n * cos(fi) * (
                    1 + (dl ** 2 / 6) * cos(fi) ** 2 * (1 - t ** 2 + n2) + (dl ** 4 / 120) * cos(fi) ** 4 * (
                        5 - 18 * t ** 2 + t ** 4 + 14 * n2 - 58 * n2 * t ** 2))
        x2000 = xgk * m0
        y2000 = ygk * m0 + ns * 1000000 + 500000
        print(f'Wynik transformacji BL -> XY do układu PL-2000 na elipsoidzie {self.model} to:\n'
              f'X = {x2000:.3f}\n'
              f'Y = {y2000:.3f}')
        return x2000, y2000

    def neu(self, xa, ya, za, xb, yb, zb):
        """
        Algorytm transformacji współrzędnych odbiornika xa, ya, za na współrzędne neu w układzie topocentrycznym na
        podstawie wspolrzednych x,y,z odbiornika i satelity.
        Parameters
        ----------
        xa, ya, za, xb, yb, zb : FLOAT
             współrzędne geodezyjne, 

        Returns
        -------
        n
            [metry] - wartosc wspolrzednej n
        e
            [metry] - wartosć wspolrzednej e
        u
            [metry] - wartosć wspolrzednej u
       
        """
        fi, lam, ha = self.xyz2flh(xa, ya, za)
        Rneu = np.array([[-np.sin(fi) * np.cos(lam),
                        -np.sin(lam),
                        np.cos(fi) * np.cos(lam)],
                         [-np.sin(fi) * np.sin(lam),
                        np.cos(lam),
                        np.cos(fi) * np.sin(lam)],
                         [np.cos(fi), 0,
                          np.sin(fi)]])
        dx = [xb - xa, yb - ya, zb - za]
        neu = Rneu.T @ dx
        print(f'Wynik transformacji XYZ -> NEU na elipsoidzie {self.model} to:\n'
              f'N = {neu[0]}\n'
              f'E = {neu[1]}\n'
              f'U = {neu[2]}')
        return neu


def wywolanie():
    parser = argparse.ArgumentParser(description='Przeliczanie współrzędnych')
    parser.add_argument('-md', '--model', type=str.lower, nargs='?', default='grs80',
                        help='Model elipsoidy odniesienia. obslugiwane modele: grs80/wgs84/krasowski, domyslny model: grs80', )
    parser.add_argument('-f', '--fun', type=str.lower, help='Nazwa wykonywanej funkcji',
                        choices=['flh2xyz', 'xyz2flh', 'pl2000', 'pl1992', 'neu'])
    parser.add_argument('-p', '--plik', type=str.lower, help='Nazwa pliku ze współrzędnymi.')
    parser.add_argument('-s', '--strefa', type=int, help='Numer strefy odwzorowawczej.', required=False)
    args = parser.parse_args()
    if args.model == 'krasowski' and (args.fun == 'pl2000' or args.fun == 'pl1992'):
        if args.fun == 'pl2000':
            print(f'Transformacja KRASOWSKI -> PL2000 nie działa poprawnie. Pomijam wykonanie obliczeń.')
        elif args.fun == 'pl1992':
            print(f'Transformacja KRASOWSKI -> PL1992 nie działa poprawnie. Pomijam wykonanie obliczeń.')
    else:
        try:
            test = Transformer(args.model)
        except:
            if args.model != ('grs80' or 'krasowski' or 'wgs84'):
                test = Transformer('grs80')
                print(f'Wybrano nieobsługiwany model elipsoidy. Wykonuje przeliczenie dla elipsoidy GRS80')
            if args.model == 'krasowski' and (args.fun == 'pl2000' or args.fun == 'pl1992'):
                print(f'Transformacja KRASOWSKI -> PL2000/PL1992 nie działa poprawnie. Pomijam wykonanie obliczeń.')
        f = open(args.plik, 'r')
        s = f.readlines()
        wsp_x = []
        wsp_y = []
        wsp_z = []
        wsp_x1 = []
        wsp_y1 = []
        wsp_z1 = []
        x_obl = []
        y_obl = []
        z_obl = []
        if args.fun == 'xyz2flh' or args.fun == 'flh2xyz' or args.fun == 'pl2000':
            for i in s:
                try:
                    if '\n' in i:
                        i = i.strip('\n')
                        i = i.strip(' ')
                        i = i.split(';')
                    else:
                        i = i.strip(' ')
                        i = i.split(';')
                    wsp_x.append(float(i[0]))
                    wsp_y.append(float(i[1]))
                    wsp_z.append(float(i[2]))
                except ValueError:
                    pass
            for i in range(0, len(wsp_x)):
                if args.fun == 'xyz2flh':
                    x, y, z = test.xyz2flh(wsp_x[i], wsp_y[i], wsp_z[i])
                    x_obl.append(x)
                    y_obl.append(y)
                    z_obl.append(z)
                elif args.fun == 'flh2xyz':
                    x, y, z = test.flh2xyz(wsp_x[i], wsp_y[i], wsp_z[i])
                    x_obl.append(x)
                    y_obl.append(y)
                    z_obl.append(z)
                elif args.fun == 'pl2000':
                    x, y = test.pl2000(wsp_x[i], wsp_y[i], int(wsp_z[i]))
                    x_obl.append(x)
                    y_obl.append(y)
        elif args.fun == 'pl1992' or args.fun == 'neu':
            for i in s:
                try:
                    if '\n' in i:
                        i = i.strip('\n')
                        i = i.strip(' ')
                        i = i.split(';')
                    else:
                        i = i.strip(' ')
                        i = i.split(';')
                    if args.fun == 'neu':
                        wsp_x.append(float(i[0]))
                        wsp_y.append(float(i[1]))
                        wsp_z.append(float(i[2]))
                        wsp_x1.append(float(i[3]))
                        wsp_y1.append(float(i[4]))
                        wsp_z1.append(float(i[5]))
                    else:
                        wsp_x.append(float(i[0]))
                        wsp_y.append(float(i[1]))
                        wsp_z.append(int(i[2]))
                except ValueError:
                    pass
            for i in range(0, len(wsp_x)):
                if args.fun == 'pl1992':
                    x, y = test.pl1992(wsp_x[i], wsp_y[i], wsp_z[i])
                    x_obl.append(x)
                    y_obl.append(y)
                elif args.fun == 'neu':
                    x = test.neu(wsp_x[i], wsp_y[i], wsp_z[i], wsp_x1[i], wsp_y1[i], wsp_z1[i])
                    x_obl.append(x[0])
                    y_obl.append(x[1])
                    z_obl.append(x[2])
        zapis = open('wsp_obliczone.txt', 'w')
        for i in range(0, len(x_obl)):
            if z_obl:
                zapis.writelines(f'{x_obl[i]} {y_obl[i]} {z_obl[i]}\n')
            else:
                zapis.writelines(f'{x_obl[i]} {y_obl[i]}\n')


if __name__ == "__main__":
    wywolanie()