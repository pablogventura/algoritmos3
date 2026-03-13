g1 = {"a":["b","d","h"],
      "b":["a","c","d","e"],
      "c":["b","d","g"],
      "d":["a","b","c"],
      "e":["b"],"f":["g"],
      "g":["c","f","h"],
      "h":["a","g"]}

g = {"a":["b","d","h"],
      "b":["a","c","d"],
      "c":["b","d","g"],
      "d":["a","b","c"],
      "f":["g"],
      "g":["c","f","h"],
      "h":["a","g"]}


g2 = {"a":["e","i"],
      "b":["d","g","h"],
      "c":["e","f","i"],
      "d":["b","g","h"],
      "e":["a","c","f"],
      "f":["c","e","i"],
      "g":["b","d"],
      "h":["b","d"],
      "i":["a","c","f"]}

p = {"a":["b","e","f"],
     "b":["a","c","g"],
     "c":["b","d","h"],
     "d":["c","e","i"],
     "e":["d","a","j"],
     "f":["a","h","i"],
     "g":["b","i","j"],
     "h":["c","j","f"],
     "i":["d","f","g"],
     "j":["e","g","h"]}

def k(vertices):
    """
    Genera un grafo completo de una determinada cantidad de vertices.
    """
    result = {}
    todos = list(map(chr, range(ord('a'), ord('a') + vertices)))
    for c in todos:
        result[c] = todos
    return result

def c(vertices):
    """
    Genera un grafo ciclo de una determinada cantidad de vertices.
    """
    result = {}
    todos = list(map(chr, range(ord('a'), ord('a') + vertices)))
    for i in range(ord('a')+1, ord('a') + vertices - 1):
        result[chr(i)]=[chr(i-1),chr(i+1)]
    result[chr(ord('a') + vertices - 1)]=['a', chr(ord('a') + vertices - 2)]
    result['a']=['b', chr(ord('a') + vertices - 1)]

    return result

def pp(g):
    """
    Genera a partir de un grafo un codigo que puede entender GraphThing, para
    graficarlo.
    """
    for v in g:
        for w in g[v]:
            print('edge "%s" -- "%s"' % (v, w))



def arbolBFS(grafo,origen):
    """
    Devuelve el arbol BFS de un grafo desde un origen dado.
    """
    q = [] # es una cola FIFO
    visitado = []
    q.append(origen)
    visitado.append(origen)
    result = {}
    for v in grafo:
        result[v] = []
    
    while q:
        v = q.pop(0) # lo toma del principio
        for w in sorted(grafo[v]):
            if w not in visitado:
                visitado.append(w)
                q.append(w) # lo inserta al final
                result[v] += [w]
                result[w] += [v]
        result[v].sort()

    return result


def arbolDFS(grafo,origen):
    """
    Devuelve el arbol DFS de un grafo desde un origen dado.
    """
    s = [] # es una pila LIFO
    visitado = []
    s.append(origen)
    visitado.append(origen)
    result={}
    for v in grafo:
        result[v] = []
    
    while s:
        v = s[-1] # lo toma del final
        agrego = False
        for w in sorted(grafo[v]):
            if w not in visitado:
                agrego = True 
                visitado.append(w)
                s.append(w) # lo inserta al final
                result[v] += [w]
                result[w] += [v]
                break
        if not agrego:
            result[v].sort() # ya esta listo, lo ordeno
            del s[-1] # lo borra porque todos sus vecinos fueron visitados
    
    return result

def ordenBFS(grafo,origen):
    """
    Devuelve el orden BFS de un grafo desde un origen dado.
    """
    q = [] # es una cola FIFO
    visitado = []
    q.append(origen)
    visitado.append(origen)
    result = []
    
    while q:
        v = q.pop(0) # lo toma del principio
        for w in sorted(grafo[v]):
            if w not in visitado:
                visitado.append(w)
                q.append(w) # lo inserta al final
                result.append((v,w))

    return visitado


def ordenDFS(grafo,origen):
    """
    Devuelve el orden DFS de un grafo desde un origen dado.
    """
    s = [] # es una pila LIFO
    visitado = []
    s.append(origen)
    visitado.append(origen)
    result = []
    
    while s:
        v = s[-1] # lo toma del final
        agrego = False
        for w in sorted(grafo[v]):
            if w not in visitado:
                agrego = True 
                visitado.append(w)
                s.append(w) # lo inserta al final
                result.append((v,w))
                break
        if not agrego:
            del s[-1] # lo borra porque todos sus vecinos fueron visitados

    return visitado

def coloreo_greedy(grafo, orden):
    """
    Devuelve un diccionario de vertices y colores, haciendo un coloreo greedy
    en algun orden dado sobre el grafo.
    """
    # hay mucho para mejorar
    result = {}
    for vertice in orden:
        result[vertice] = None
    
    ultimocolor = 1
    for vertice in orden:
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
    
    return result


def nivelesBFS(grafo,origen):
    """
    Devuelve un diccionario con los niveles y vertices del arbol BFS de un grafo desde un origen dado.
    """
    q = [] # es una cola FIFO
    visitado = []
    q.append((origen,0))
    visitado.append(origen)
    result = {0:[origen]}
    
    while q:
        v,nivel = q.pop(0) # lo toma del principio
        
        for w in sorted(grafo[v]):
            if w not in visitado:
                visitado.append(w)
                q.append((w,nivel+1)) # lo inserta al final
                try:
                    result[nivel+1] += [w]
                except KeyError:
                    result[nivel+1] = [w]

    return result

def esPropio(grafo,coloreo):
    """
    Devuelve si el coloreo (un dict de vertices con colores) es propio en el grafo.
    """
    for v in grafo:
        for w in grafo[v]:
            if coloreo[v]==coloreo[w]:
                return False
    return True

def coloreo_bipartito(grafo):
    """
    Devuelve un coloreo de dos colores, solo es propio si el grafo es bipartito.
    """
    result = {}
    niveles = nivelesBFS(grafo,"a")
    for nivel in niveles:
        for v in niveles[nivel]:
            result[v] = nivel % 2
    
    return result

def coloreo_menoroigual_maxval(grafo):
    """
    Si el grafo no es regular, devuelve un coloreo propio usando una cantidad
    de colores menor o igual a la maxima valencia del grafo.
    """
    cantv = {len(grafo[v]):v for v in grafo}
    
    v = cantv[min(cantv)]
    
    orden = ordenBFS(grafo,v)
    orden.reverse()
    
    return coloreo_greedy(grafo, orden)


def coloreo_polinomico(grafo):
    """
    Dar un algoritmo polinomial que resuelva el siguiente problema:
    Input: Un grafo G que se garantiza que es no regular con maxval
    menor o igual a  3.
    Output: Su algoritmo debe dar X(G) y un coloreo propio con X(G) colores.
    (nota: para probar que es polinomial debe dar su complejidad).
    """


    col2 = coloreo_bipartito(grafo)
    
    if esPropio(grafo,col2):
        return (2,col2)
    else:
        # tiene un ciclo impar
        # pero como X(G) < maxval que es igual a 3,X(G) = 3
        col3 = coloreo_menoroigual_maxval(grafo)
        assert esPropio(grafo,col3)
        return (3, col3)
    
    




def grafo10(n):
    result = {}
    
    for i in range(n):
        for j in range(n):
            result[(i,j)] = []
    
    for i in range(n):
        for j in range(n):
            horizontales = [(i1,j) for i1 in range(n)]
            horizontales.remove((i,j))
            verticales   = [(i,j1) for j1 in range(n)]
            verticales.remove((i,j))
            
            diagas = []
            for i1 in range(n):
                for j1 in range(n):
                    if i + j == i1 + j1:
                        diagas += [(i1,j1)]
            diagas.remove((i,j))

            diagdes = []
            for i1 in range(n):
                for j1 in range(n):
                    if i - j == i1 - j1:
                        diagdes += [(i1,j1)]
            diagdes.remove((i,j))
            
            result[(i,j)]= horizontales + verticales + diagas + diagdes
    
    return result
    
    
def grafo10pp(n):
    for i in range(n):
        l = []
        for j in range(n):
            l.append((i,j))
        print(l)
    
def coloreo10(grafo,n):
    result = {}
    for (i,j) in grafo:
        result[(i,j)] = (j-2*i)%n
    return result
    
    
    
def pruebomuchoal10(maximo):

    for n in range(maximo):
        g = grafo10(n)
        cg = coloreo10(g,n)
        print((n%6==1 or n%6==5,esPropio(g,cg)))


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
