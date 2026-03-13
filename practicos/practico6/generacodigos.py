import codigos
import math
import itertools
import numpy

def todascolumnas(n,m):
    result = []
    for col in list(itertools.product(*(([codigos.z2(0),codigos.z2(1)],)*m))):
        col = codigos.matrix(col)
        if codigos.w(col)>1:
            col = col.transpose()
            result.append(col)
    result = numpy.concatenate(result,1)
    result = (result.transpose()[:n]).transpose()
    return result
         
            


def resuelve(fun,val):
    x=0
    while not fun(x) >= val:
        x+=1
    return x

def generaChequeoCodigo(cant):
    k = int(math.ceil(math.log(cant,2)))
    x = resuelve(lambda x:2**x-1-x,k)
    i = codigos.identidad(x)
    result = numpy.concatenate((i,todascolumnas(k,x)),1)
    return result
