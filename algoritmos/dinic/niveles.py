#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
BFS de niveles en la red residual (Dinic).
Calcula la distancia desde la fuente hasta cada vértice; devuelve None si el sumidero no es alcanzable.
"""

from collections import deque

from red import RedDinic, arista


def bfs_niveles(red):
    """
    BFS en la red residual desde la fuente. Solo se siguen aristas con capacidad residual.
    Devuelve dict vértice -> nivel (entero), o None si el sumidero no es alcanzable.
    """
    nivel = {red.FUENTE: 0}
    cola = deque([red.FUENTE])

    while cola:
        v = cola.popleft()
        lv = nivel[v]
        # Aristas salientes con capacidad residual
        for w in red.vecinos_mas(v):
            if red.residual(v, w) <= 0:
                continue
            if w not in nivel:
                nivel[w] = lv + 1
                cola.append(w)
                if w == red.SUMIDERO:
                    return nivel
        # Aristas entrantes (reversas) con flujo > 0
        for u in red.vecinos_menos(v):
            if red.flujo_arista(u, v) <= 0:
                continue
            if u not in nivel:
                nivel[u] = lv + 1
                cola.append(u)

    return nivel if red.SUMIDERO in nivel else None
