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

    def xyz2flh(self, x, y, z):
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
        n = nn(fi, self.a, self.e2)
        x = (n + h) * cos(fi) * cos(la)
        y = (n + h) * cos(fi) * sin(la)
        z = (n + h - n * self.e2) * sin(fi)
        print(f'Wynik transformacji BLH -> XYZ na elipsoidzie {self.model} to:\n'
              f'X = {x:.3f}\n'
              f'Y = {y:.3f}\n'
              f'Z = {z:.3f}')
        return x, y, z


test = Transformer('grs80')
fia, lama, ha = test.xyz2flh(3850700.000, 1658260.000, 4790660.000)
test.flh2xyz(fia, lama, ha)

# TODO 1 - przerobic dms tak zeby pokazywal wynik ze znakiem stopien, minuta, sekunda
# TODO 2 - dodać transformacje do pl2000, pl1992, rneuy
