import numpy as np
from math import *
def Np(f, a, e2):

    N = a / np.sqrt(1 - e2 * sin(f)**2)
    return(N)

def Mp(f,a,e2):
    M = a * (1-e2) / np.sqrt((1-e2 * np.sin(f)**2)**3)
    return(M)
class Tranformer():
    def __init__(self, model):
        # if model == 'grs80':

    def xyz2flh(self, X, Y, Z, a, e2):
    P = sqrt(X**2 + Y**2)
    f = np.arctan(Z/(P*(1 - e2)))

    while True:
        N = Np(f, a, e2)
        h = P / cos(f) - N
        fp = f
        f = np.arctan(Z/(P* (1 - e2 * N / (N + h))))
        if abs(fp - f) < (0.000001/206265):
            break

    l = np.arctan2(Y, X)
    return(f, l, h)

    def flh2xyz(self, f, l, h, a, e2):
    N = Np(f, a, e2)
    X = (N + h) * cos(f) * cos(l)
    Y = (N + h) * cos(f) * sin(l)
    Z = (N + h - N * e2) * sin(f)
    return(X, Y, Z)





