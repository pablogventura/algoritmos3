"""
Red de flujo con aristas en formato "xy" (ej. "0A", "F1").
Funciones para vecinos, red residual (na) y niveles (BFS).
Fuente "0", sumidero "1".
"""
from collections import deque
from functools import reduce

# Ejemplo: capacidades por arista (clave "xy" = arista de x a y)
nw = {
    "0C":7,
    "0D":10,
    "0E":7,
    "AF":4,
    "AG":3,
    "AI":8,
    "CG":2,
    "CH":3,
    "CJ":5,
    "DF":4,
    "DG":2,
    "EF":3,
    "EG":5,
    "EH":4,
    "F1":7,
    "G1":5,
    "H1":4,
    "I1":9,
    "J1": 15,
}


def vecinosMas(v, n):
    """Vecinos salientes de v cuando n es un dict arista_str -> capacidad (ej. "0A" -> 8)."""
    return sorted({arista[1] for arista in n if len(arista) >= 2 and arista[0] == v})


def vecinosMenos(v, n):
    """Vecinos entrantes de v cuando n es un dict arista_str -> capacidad."""
    return sorted({arista[0] for arista in n if len(arista) >= 2 and arista[1] == v})


def na(c, f):
    """
    Red residual (niveles) desde "0" hacia "1".
    c, f: dict arista_str -> capacidad / flujo. Devuelve dict arista -> (residual, es_backward).
    """
    result = {}
    visitado = {"0": 0}
    cola = deque(["0"])

    while cola:
        v = cola.popleft()
        for w in vecinosMas(v, c):
            if ("1" not in visitado or w == "1") and (w not in visitado or visitado[w] == visitado[v] + 1):
                if c.get(v + w, 0) - f.get(v + w, 0) > 0:
                    visitado[w] = visitado[v] + 1
                    cola.append(w)
                    result[v + w] = (c[v + w] - f.get(v + w, 0), False)
        for w in vecinosMenos(v, c):
            if ("1" not in visitado or w == "1") and (w not in visitado or visitado[w] == visitado[v] + 1):
                if f.get(w + v, 0) > 0:
                    visitado[w] = visitado[v] + 1
                    cola.append(w)
                    result[v + w] = (f[w + v], True)

    return result


def arbolBFS(grafo):
    """
    Árbol BFS del grafo desde "0". grafo: dict arista_str -> capacidad (solo se usan las claves).
    Devuelve dict vértice -> lista de vecinos en el árbol.
    """
    visitado = {"0"}
    cola = deque(["0"])
    result = {v: [] for v in set(k[0] for k in grafo) | set(k[1] for k in grafo)}

    while cola:
        v = cola.popleft()
        for w in vecinosMas(v, grafo):
            if w not in visitado:
                visitado.add(w)
                cola.append(w)
                result[v].append(w)
                result[w].append(v)
        result[v].sort()

    return result

def soloprim(lista):
    """Elimina duplicados preservando el orden de primera aparición."""
    seen = set()
    return [x for x in lista if x not in seen and not seen.add(x)]


def niveles(n):
    """
    Niveles BFS desde "0" en la red n (dict arista_str -> valor).
    result[i] = lista de vértices a distancia i.
    """
    result = [["0"]]
    todos = set(k[0] for k in n) | set(k[1] for k in n)
    while set(reduce(lambda a, b: a + b, result)) != todos:
        temp = []
        for x in result[-1]:
            temp.extend(vecinosMas(x, n))
        result.append(soloprim(temp))
    return result

def wave(n):
    """
    Algoritmo wave (flujo en niveles). n: dict arista_str -> capacidad.
    Calcula red residual, niveles, y devuelve niveles. (Parte final por completar.)
    """
    c = dict(n)
    f = {k: 0 for k in c}
    vertices = set(x[0] for x in n) | set(x[1] for x in n)
    b = {k: False for k in vertices}
    emu = {k: [] for k in vertices}
    aux = na(c, f)
    niv = niveles(aux)
    l = reduce(lambda x, y: x + y, niv)
    if not l:
        return niv
    v = l[0]
    for w in vecinosMas(v, aux):
        if not b.get(w, False):
            arista_vw = v + w
            delta = c.get(arista_vw, 0) - f.get(arista_vw, 0)
            if delta > 0:
                f[arista_vw] = f.get(arista_vw, 0) + delta
                emu[w].append((emu.get(v, [])[-1] if emu.get(v) else 0) + delta)
    return niv
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
