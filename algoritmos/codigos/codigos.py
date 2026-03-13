"""
Códigos lineales sobre Z₂: clase z2, matrices, conversión y matriz de chequeo.
"""
import itertools
import numpy
from numpy import concatenate, matrix, shape, transpose


class z2(object):
    """Elemento del cuerpo Z₂ (entero módulo 2). Soporta +, -, *, ==."""

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
    """Todas las cadenas binarias de longitud n (orden lexicográfico)."""
    return ["".join(t) for t in itertools.product(*(("01",) * n))]


def identidad(n):
    """Matriz identidad n×n con entradas en Z₂."""
    temp = numpy.identity(n).tolist()
    return matrix([[z2(int(x)) for x in fila] for fila in temp])

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

