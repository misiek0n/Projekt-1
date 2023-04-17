import numpy as np
from math import *
def nn(f, a, e2):
    n = a / np.sqrt(1 - e2 * sin(f)**2)
    return(n)

def mp(f,a,e2):
    M = a * (1-e2) / np.sqrt((1-e2 * np.sin(f)**2)**3)
    return(M)
class Transformer():
    def __init__(self, model):
        if model == 'grs80':
            self.a = 6378137
            self.e2 = 0.00669438002290
        elif model == 'wgs84':
            self.a = 6378137
            self.e2 = 0.0033528106647474805

    def xyz2flh(self, X, Y, Z):
        P = sqrt(X**2 + Y**2)
        f = np.arctan(Z/(P*(1 - self.e2)))

        while True:
            n = nn(f, self.a, self.e2)
            h = P / cos(f) - n
            fp = f
            f = np.arctan(Z/(P* (1 - self.e2 * n / (n + h))))
            if abs(fp - f) < (0.000001/206265):
                break
    
            l = np.arctan2(Y, X)
            return f, l, h

    def flh2xyz(self, f, l, h):
        N = nn(f, self.a, self.e2)
        X = (N + h) * cos(f) * cos(l)
        Y = (N + h) * cos(f) * sin(l)
        Z = (N + h - N * self.e2) * sin(f)
        return X, Y, Z





