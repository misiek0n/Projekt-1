import numpy as np
from math import *


def nn(f, a, e2):
    n = a / np.sqrt(1 - e2 * sin(f)**2)
    return n


def mp(f, a, e2):
    m = a * (1-e2) / np.sqrt((1-e2 * np.sin(f)**2)**3)
    return m


class Transformer:
    def __init__(self, model):
        if model == 'grs80':
            self.a = 6378137
            self.e2 = 0.00669438002290
        elif model == 'wgs84':
            self.a = 6378137
            self.e2 = 0.00669438
        elif model == 'krasowski':
            self.a = 6378245
            self.e2 = 0.00669342

    def xyz2flh(self, x, y, z):
        p = sqrt(x**2 + y**2)
        fi = np.arctan(z/(p*(1 - self.e2)))

        while True:
            n = nn(fi, self.a, self.e2)
            h = p / cos(fi) - n
            fp = fi
            fi = np.arctan(z/(p * (1 - self.e2 * n / (n + h))))
            if abs(fp - fi) < (0.000001/206265):
                break
            la = np.arctan2(y, x)
            return fi, la, h

    def flh2xyz(self, fi, la, h):
        n = nn(fi, self.a, self.e2)
        x = (n + h) * cos(fi) * cos(la)
        y = (n + h) * cos(fi) * sin(la)
        z = (n + h - n * self.e2) * sin(fi)
        return x, y, z
