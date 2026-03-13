"""
Códigos cíclicos: polinomios generadores, matrices generadora y de chequeo,
codificación y corrección de errores (síndromes).
"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "codigos")))
import numpy
import sympy
import codigos

x = sympy.var("x")


# Polinomios generadores y longitud n del código (ejercicios)
ga, na = 1 + x + x**3, 7
gb, nb = 1 + x**2 + x**3, 7
gc, nc = 1 + x**3 + x**4, 15
gd, nd = 1 + x + x**4, 15
ge, ne = 1 + x**2 + x**4 + x**6 + x**7 + x**10, 21
gf, nf = 1 + x + x**5 + x**6 + x**7 + x**9 + x**11, 23
gh, nh = 1 + x**4 + x**6 + x**7 + x**8, 15



def z2Pol(p):
    result = corrigeCoef(p,grado(p)+1)
    result = sympy.Poly(reversed(result),x)/1
    return result

def corrigeCoef(dp, n):
    """Lista de n coeficientes en Z₂ del polinomio dp (índice 0 = término constante)."""
    coef = dp.as_coefficients_dict()
    return [codigos.z2(coef.get(x**i, 0)) for i in range(n)]
    
def grado(p):
    try:
        return sympy.degree(p)
    except sympy.ComputationFailed:
        return 0

def restoPol(p,g):
    """Resto de p divivido g"""
    result = {}
    cociente,resto = sympy.div(p,g,x)

    return resto

def dimension(g,n):
    return n-grado(g)

def matrizGeneradora(g,n):
    result = []
    for i in range(n-dimension(g,n),n):
        temp = restoPol(x**i,g) + x**i
        result.append(corrigeCoef(temp,n))
    return codigos.matrix(result)

def aChequeo(gen):
    n,m=numpy.shape(gen)
    a = numpy.transpose(gen[:,range(abs(n-m))])
    i = codigos.identidad(len(a))
    return numpy.concatenate((i,a),axis=1)

def codifica1(g,n,w):
    assert grado(w) <= dimension(g,n)
    temp = corrigeCoef((g*w).expand(),n)
    temp = sympy.Poly(reversed(temp),x)
    return temp

def codifica2(g,n,w):
    k = dimension(g,n)
    assert grado(w) <= dimension(g,n)
    temp = restoPol(x**(n-k) * w,g) + (x**(n-k) * w)
    temp = temp.expand()
    temp = corrigeCoef(temp,n)
    temp = sympy.Poly(reversed(temp),x)
    return temp

def ejercicio1(g,n,w1,w2):
    print("-" * 80)
    print("g=%s" % g)
    print("n=%s" % n)
    print("")
    print("k=%s" % dimension(g,n))
    print("")
    print("Matriz Generadora")
    print(matrizGeneradora(g,n))
    print("")
    print("Matriz de Chequeo")
    print(aChequeo(matrizGeneradora(g,n)))
    print("")
    print("(x**n+1)/g(x)=%s" % restoPol(g,x**n+1))
    print("")
    print("Codificacion metodo 1, primer palabra")
    print("Original: %s - Codificada: %s" % (w1,codifica1(g,n,w1)/1))
    print("Codificacion metodo 1, segunda palabra")
    print("Original: %s - Codificada: %s" % (w2,codifica1(g,n,w2)/1))
    print("Codificacion metodo 2, primer palabra")
    print("Original: %s - Codificada: %s" % (w1,codifica2(g,n,w1)/1))
    print("Codificacion metodo 2, segunda palabra")
    print("Original: %s - Codificada: %s" % (w2,codifica2(g,n,w2)/1))

def resolvere1():
    w1=x**3
    w2=x**2+x**3
    print("")
    print("Ej 1a")
    ejercicio1(ga,na,w1,w2)
    print("")
    print("Ej 1b")
    ejercicio1(gb,nb,w1,w2)
    print("")
    print("Ej 1c")
    ejercicio1(gc,nc,w1,w2)
    print("")
    print("Ej 1d")
    ejercicio1(gd,nd,w1,w2)
    print("")
    print("Ej 1e")
    ejercicio1(ge,ne,w1,w2)
    print("")
    print("Ej 1f")
    ejercicio1(gf,nf,w1,w2)
    print("")
    print("Ej 1g")
    ejercicio1(gh,nh,w1,w2)


def polStr(p,n):
    nada=""
    return nada.join(map(str,corrigeCoef(p,n)))

def strPol(s):
    s = list(s)
    s = map(int,s)
    return sympy.Poly(reversed(s),x)/1


def errortrap(g,n,t,w):

    print("Llego w(x) = %s" % w)
    s=[]
    so=[]
    for i in range(0,n):
        so.append(restoPol(x**i*w,g))
    print("\nSs = ")
    for si in so:
        print(z2Pol(si))
    print("")
    so = map(lambda arg:corrigeCoef(arg,n),so)
    s = map(lambda arg:arg.count(codigos.z2(1)),so)
    huboerror = False
    for j in range(t,-1,-1):
        if j in s:
            i = s.index(j)
            huboerror = True
            break
    if huboerror:
        if 0 in s:
            print("no hubo error!")
            v = w
            print("V(x) = W(x)")
            
            H = aChequeo(matrizGeneradora(g,n))
            chek = (H*codigos.convertir(polStr(w,n)))
            assert all(map(lambda _:_.valor==0,chek.transpose().tolist()[0]))
            print("Chequeo bien! H*v'===0")
            return v
        print("               i = %s" % i)
        si = sympy.Poly(reversed(so[i]),x)/1
        print("          S_%s(x) = %s" % (i,si))
        e = restoPol(x**(n-i)*si,1+x**n)
        print("            E(x) = %s" % z2Pol(e))
        v = w + e
        print("V(x) = W(x)+E(x) = %s" % z2Pol(v))
        
        H = aChequeo(matrizGeneradora(g,n))
        chek = (H*codigos.convertir(polStr(v,n)))
        assert all(map(lambda _:_.valor==0,chek.transpose().tolist()[0]))
        print("Chequeo bien! H*v'==0")
        return v
    else:
        print("Hubo error al mandar, pero no corregible!")
        v = w
        print("V(x) = W(x)")
        
        H = aChequeo(matrizGeneradora(g,n))
        chek = (H*codigos.convertir(polStr(w,n)))
        assert not all(map(lambda _:_.valor==0,chek.transpose().tolist()[0]))
        print("Chequeo bien! H*v'!=0")
        return v

    
def resolvere2():
    g=1+x**4+x**6+x**7+x**8
    n = 15
    t = 2
    wa = "001000001110110"
    wb = "110010011110111"
    wc = "001111101001001"
    wd = "001000000110000"
    we = "110001101000101"
    wf = "001001000100110"
    print("generador = %s" % g)
    print("n = %s" % n)
    print("t = %s" % t)
    print("")
    for w in [wa,wb,wc,wd,we,wf]:
        print("-" * 80)
        print("Llego %s" % w)
        v = errortrap(g,n,t,strPol(w))
        print("Quedo %s" % polStr(v,n))
        print("-" * 80)
    
    
    
    
