import numpy as np
from math import *


def nn(f, a, e2):
    n = a / np.sqrt(1 - e2 * sin(f)**2)
    return n


def mp(f, a, e2):
    m = a * (1-e2) / np.sqrt((1-e2 * np.sin(f)**2)**3)
    return m


def dms(x):
    znak = ' '
    if x < 0:
        znak = '-'
        x = abs(x)
    x = x * 180/pi
    d = int(x)
    m = int((x - d) * 60)
    s = (x - d - m/60) * 3600
    print(znak, "%3d %2d %7.5f" % (d, m, s))


class Transformer:
    def __init__(self, model):
        self.model = model
        if model == 'grs80':
            self.a = 6378137
            self.e2 = 0.00669438002290
        elif model == 'wgs84':
            self.a = 6378137
            self.e2 = 0.00669438
        elif model == 'krasowski':
            self.a = 6378245
            self.e2 = 0.00669342162296
        else:
            raise NotImplementedError(f"{model} nie ma takiego modelu :( ")

    def xyz2flh(self, x, y, z):
        if __name__ == "__main__":
            p = sqrt(x ** 2 + y ** 2)
            fi = np.arctan(z / (p * (1 - self.e2)))

            while True:
                n = nn(fi, self.a, self.e2)
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
            return fi, la, h

    def flh2xyz(self, fi, la, h):
        if __name__ == "__main__":
            n = nn(fi, self.a, self.e2)
            x = (n + h) * cos(fi) * cos(la)
            y = (n + h) * cos(fi) * sin(la)
            z = (n + h - n * self.e2) * sin(fi)
            print(f'Wynik transformacji BLH -> XYZ na elipsoidzie {self.model} to:\n'
                  f'X = {x:.3f}\n'
                  f'Y = {y:.3f}\n'
                  f'Z = {z:.3f}')
            return x, y, z

    def pl1992(self, fi, lam):
        if __name__ == "__main__":
            lam0 = radians(19)
            m0 = 0.9993
            b2 = self.a ** 2 * (1 - self.e2)
            ep2 = (self.a ** 2 - b2) / b2
            dl = lam - lam0
            t = tan(fi)
            n2 = ep2 * cos(fi) ** 2
            n = nn(fi, self.a, self.e2)
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

    def pl2000(self, fi, lam):
        if __name__ == "__main__":
            if lam <= 16.5:
                l0 = radians(15)
                ns = 5
            elif 16.5 < lam <= 19.5:
                l0 = radians(18)
                ns = 6
            elif 19.5 < lam <= 22.5:
                l0 = radians(21)
                ns = 7
            elif lam > 22.5:
                l0 = radians(24)
                ns = 8
            m0 = 0.999923
            lam = radians(lam)
            fi = radians(fi)
            b2 = self.a ** 2 * (1 - self.e2)
            ep2 = (self.a ** 2 - b2) / b2
            dl = lam - l0
            t = tan(fi)
            n2 = ep2 * cos(fi) ** 2
            n = nn(fi, self.a, self.e2)
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
        if __name__ == "__main__":
            dwsp = np.array([xb - xa, yb - ya, zb - za])
            fi, lam, ha = self.xyz2flh(xa, ya, za)
            r = np.array([[-sin(fi) * cos(lam), -sin(lam), cos(fi) * cos(lam)],
                          [-sin(fi) * sin(lam), cos(lam), cos(fi) * sin(lam)],
                          [cos(fi), 0, sin(fi)]])
            dx = r.T @ dwsp
            n = dx[1]
            wektor_e = dx[0]
            u = dx[2]
            print(f'Wynik transformacji XYZ -> NEU na elipsoidzie {self.model} to:\n'
                  f'N = {n:.3f}\n'
                  f'E = {wektor_e:.3f}\n'
                  f'U = {u:.3f}')


test = Transformer('grs80')
fiaa, lamaa, haa = test.xyz2flh(3850700.000, 1658260.000, 4790660.000)
test.flh2xyz(fiaa, lamaa, haa)
lamd = degrees(lamaa)
fid = degrees(fiaa)
test.pl2000(fid, lamd)
test.neu(3850700.000, 1658260.000, 4790660.000, 3855141.595, 1626409.701, 1626409.701)


# TODO 1 - przerobic dms tak zeby pokazywal wynik ze znakiem stopien, minuta, sekunda
# TODO 2 - pl2000 przyjmuje wartości w stopniach, pl1992 w radianach, najprawdopodobniej trzeba to sprowadzić do tych
#          samych jednostek
