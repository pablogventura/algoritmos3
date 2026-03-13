import numpy

from numpy import matrix
from numpy import transpose
from numpy import shape
from numpy import concatenate
import itertools

class z2(object):
    def __init__(self, valor):
        self.valor = int(valor) % 2
    def __add__(self, otro):
        return z2((self.valor + otro.valor)%2)
    def __sub__(self, otro):
        return z2((self.valor - otro.valor)%2)
    def __mul__(self, otro):
        return z2((self.valor * otro.valor)%2)
    def __str__(self):
        return str(self.valor)
    def __repr__(self):
        return str(self)
    def __eq__(self, otro):
        return (self.valor%2 == otro.valor%2)
    def __ne__(self, otro):
        return not (self == otro)


def recorre(n):
    result = list(itertools.product(*(("01",)*n))) # asterisco para *args
    result = map("".join,result)
    return result

        

def identidad(n):
    temp = numpy.identity(n)
    temp = temp.tolist()
    result = []
    for fila in temp:
        nfila = map(int,fila)
        nfila = map(z2,fila)
        result.append(nfila)
    return matrix(result)

def _convertir(cadena):
    result = list(cadena)
    result = map(int,result)
    result = map(z2,result)
    return result

def convertir(lcadenas):
    return matrix(map(_convertir,lcadenas)) #,dtype=numpy.bool)
    
def aChequeo(gen):
    n,m=shape(gen)
    a = transpose(gen[:,range(min(n,m),max(n,m))])
    i = identidad(len(a))
    return concatenate((a,i),axis=1)


def w(palabra):
    return palabra.tolist()[0].count(z2(1))

g3 = ["100001100",
      "010001010",
      "001000111",
      "000101110",
      "000010101"]
g3 = convertir(g3)


h4 = ["10001010",
      "01001111",
      "00100011",
      "00011100"]
h4 = convertir(h4)

g4 = ["11011000",
      "01010100",
      "11100010",
      "01100001"]
g4 = convertir(g4)

g5 = ["11000100000000",
      "10101010000000",
      "01101001000000",
      "11100000100000",
      "10010000010000",
      "01011000001000",
      "11010000000100",
      "00110000000010",
      "10111000000001"]
g5=convertir(g5)

h5=["10000110110101",
    "01000101101100",
    "00100011100011",
    "00010000011111",
    "00001011001001"]
h5=convertir(h5)

