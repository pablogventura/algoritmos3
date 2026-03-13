g = {"a" :["b", "e"],
     "b" :["a", "c", "d"],
     "c" :["b", "e"],
     "d" :["b", "f", "g"],
     "e" :["a", "c", "g"],
     "f" :["b", "d", "g"],
     "g" :["d", "e", "f", "h"],
     "h" :["g", "i1", "i2", "i3", "i4", "i5", "i6"],
     "i1":["h", "j1", "j2", "j3", "j4", "j5", "j6", "j7"],
     "i2":["h"],
     "i3":["h"],
     "i4":["h"],
     "i5":["h"],
     "i6":["h"],
     "j1":["i1"],
     "j2":["i1"],
     "j3":["i1"],
     "j4":["i1"],
     "j5":["i1"],
     "j6":["i1"],
     "j7":["i1"],
     }
# TODO un network podria ser un diccionario como el de grafos, poniendo en "a",
# los vertices a los que se llega desde "a" (para indicar el sentido) en una
# tupla junto con la capacidad de la arista


import probando
def rlf(grafo):
    """
    Devuelve un coloreo propio usando la heuristica RLF
    """
    result = {}
    color = 1
    print("color %s" % color)
    R = set(grafo.keys())  # Vertices no coloreados
    print("R = %s" % R)
    while R:
        L = set(R)
        iteracion = 0
        print("L = %s" % L)
        while L:
            print("    iteracion %s" % iteracion)

            temp = {v: len(set(grafo[v]).intersection(R)) for v in L}
            temp1 = list(filter(lambda x: temp[x] == max(temp.values()), temp))
            v = ordena(temp1, grafo)[0]

            print("    tomo %s de L" % v)
            #v = max(L,key=lambda v: len(set(grafo[v]).intersection(R)))
            result[v] = color
            R.discard(v)
            L = L - set(grafo[v] + [v])
            print("    R = %s" % R)
            print("    L = %s" % L)
            iteracion += 1
            print("-------------")
        print("termine con ese color")
        color += 1
        print("color %s" % color)
    return result

def greedy(grafo,orden):
    result = {}
    
    for v in orden:
        result[v] = paso_greedy(grafo, result, v)
    
    return result

def paso_greedy(grafo, coloreoparcial, vertice):
    """
    Devuelve un diccionario de vertices y colores, haciendo un coloreo greedy
    en algun orden dado sobre el grafo.
    """
    # hay mucho para mejorar
    result = {}
    for v in sorted(grafo.keys()):
        try:
            result[v] = coloreoparcial[v]
        except Exception:
            result[v] = None
    try:
        ultimocolor = max(coloreoparcial.values())
    except Exception:
        ultimocolor = 1

    coloresvecinos = []
    for vecino in grafo[vertice]:
        if result[vecino]:
            coloresvecinos.append(result[vecino])
    coloresdisponibles = set(range(1,ultimocolor+1)) - set(coloresvecinos)
    
    if coloresdisponibles:
        result[vertice] = sorted(coloresdisponibles)[0]
    else:
        result[vertice] = ultimocolor + 1
        ultimocolor += 1
    
    return result[vertice]

def coloresvecinos(grafo,coloreo,v):
    result = set()
    for vecino in grafo[v]:
        try:
            result.add(coloreo[vecino])
        except Exception:
            pass
            #print "el vertice %s no estaba coloreado" % vecino
    return result

def v_coloresvecinos(grafo,coloreo):
    """
    Devuelve una lista de vertices no coloreados con mas colores vecinos.
    """
    result = {}
    for v in grafo.keys():
        result[v] = []
        for w in grafo[v]:
            if w in coloreo.keys():
                result[v].append(coloreo[w])
        result[v] = len(set(result[v]))
    for v in coloreo.keys():
        if v in result.keys():
            del result[v]
    return list(filter(lambda x: result[x] == max(result.values()), result.keys()))

def dsatur(grafo):
    result = {}
    orden = []
    result[ordena(grafo.keys(),grafo)[0]] = paso_greedy(grafo, result, ordena(grafo.keys(),grafo)[0]) # empiezo con la primer letra
    orden.append(ordena(grafo.keys(),grafo)[0])
    for i in range(len(grafo)-1):
        d5 = ordena(v_coloresvecinos(grafo,result),grafo)
        m = d5[0]
        result[m] = paso_greedy(grafo, result, m)
        orden.append(m)
    print(orden)
    return result

def subgrafo(grafo, vertices):
    result = {}
    for v in grafo:
        if v not in vertices:
            result[v] = sorted(set(grafo[v]) - set(vertices))
    return result

def wpmod(grafo):
    result = {}
    orden = []
    result[ordena(grafo.keys(),grafo)[0]] = paso_greedy(grafo, result,ordena(grafo.keys(),grafo)[0] ) # empiezo con la primer letra
    orden.append(ordena(grafo.keys(),grafo)[0])
    for i in range(len(grafo)-1):
        sg = subgrafo(grafo,result.keys())
        m = ordena(sg.keys(),sg)[0]

        result[m] = paso_greedy(grafo, result, m)
        orden.append(m)
    print(orden)
    return result


def _vgrado(grado, grafo):
    """
    Devuelve los vertices de ese grado en el grafo, ordenados alfabeticamente.
    """    
    result = []
    for v in grafo:
        if len(grafo[v]) == grado:
            result.append(v)
    result.sort()
    return result
    
def ordena(lista,grafo):
    """
    Ordena la lista de vertices, por grado, y cuando empatan, alfabeticamente.
    """
    result = []
    grado = max([len(grafo[v]) for v in grafo])
    for i in range(grado+1,-1,-1):
        result += _vgrado(i,grafo)
    return list(filter(lambda x: x in lista, result))

    
    
    
