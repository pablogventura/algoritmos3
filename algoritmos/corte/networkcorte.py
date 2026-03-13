"""
Corte mínimo en una red de flujo.
Convierte la red (vértice -> [(vecino, capacidad)]) en grafo + capacidades,
y calcula el conjunto S del corte (vértices alcanzables por BFS en la red residual).
"""

from collections import deque

# Ejemplo: red con fuente "s", sumidero "t"
n = {"s": [("a", 4), ("c", 4)],
     "a": [("b", 4), ("d", 2)],
     "c": [("b", 2), ("d", 4)],
     "b": [("t", 4)],
     "d": [("t", 2)],
     "t": []}

f = {("s", "a"): 4,
     ("s", "c"): 2,
     ("a", "b"): 4,
     ("a", "d"): 0,
     ("c", "b"): 0,
     ("c", "d"): 2,
     ("b", "t"): 4,
     ("d", "t"): 2}


def ntog(network):
    """
    Convierte la red (dict vértice -> [(vecino, cap)]) en (grafo, capacidades).
    grafo[v] = lista ordenada de vecinos; c[(v,w)] = capacidad.
    """
    g = {}
    c = {}
    for v in network:
        g[v] = []
        for (w, cap) in network[v]:
            g[v].append(w)
            c[(v, w)] = cap
        g[v].sort()
    return (g, c)


def corteminimal(network, f):
    """
    Conjunto S de un corte mínimo: vértices alcanzables desde "s" en la red residual.
    BFS desde "s": se sigue (v,w) si capacidad residual c[(v,w)] - f[(v,w)] > 0.
    """
    grafo, c = ntog(network)
    visitado = {"s"}
    cola = deque(["s"])

    while cola:
        v = cola.popleft()
        for w in grafo[v]:
            if w not in visitado and c[(v, w)] > f.get((v, w), 0):
                visitado.add(w)
                cola.append(w)

    return list(visitado)

def capacidadCorte(corte, network, f):
    """Capacidad del corte (conjunto S = corte): suma de f(v,w) con v en S, w no en S."""
    g, c = ntog(network)
    corte_set = set(corte)
    return sum(
        f.get((v, w), 0)
        for v in g
        if v in corte_set
        for w in g[v]
        if w not in corte_set
    )


def valorFlujo(f, network):
    """Valor del flujo: suma del flujo que sale de la fuente "s" (menos lo que entra en "t" desde otros)."""
    g, _ = ntog(network)
    return sum(f.get((v, "t"), 0) for v in g if "t" in g[v])












