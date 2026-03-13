"""
Generación de matrices de chequeo para códigos.
"""
import itertools
import math
import numpy
import codigos


def todascolumnas(n, m):
    """Columnas binarias de longitud m con peso > 1, truncadas a n columnas."""
    result = []
    for col in itertools.product(*([codigos.z2(0), codigos.z2(1)] for _ in range(m))):
        col = codigos.matrix(col)
        if codigos.w(col) > 1:
            result.append(col.transpose())
    if not result:
        return numpy.empty((m, 0))
    result = numpy.concatenate(result, 1)
    return (result.transpose()[:n]).transpose()


def resuelve(fun, val):
    """Mínimo x tal que fun(x) >= val."""
    x = 0
    while fun(x) < val:
        x += 1
    return x

def generaChequeoCodigo(cant):
    """Matriz de chequeo (paridad) para un código con al menos `cant` palabras."""
    k = int(math.ceil(math.log(cant, 2)))
    x = resuelve(lambda n: 2**n - 1 - n, k)
    i = codigos.identidad(x)
    return numpy.concatenate((i, todascolumnas(k, x)), 1)
