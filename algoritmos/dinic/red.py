#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Red de flujo para Dinic: capacidades, flujos y listas de adyacencia precomputadas.
Permite vecinos en O(1) y evita recorrer todas las aristas en cada BFS/DFS.
"""


def arista(v, w):
    """Clave de arista (inmutable) para vértices de cualquier longitud."""
    return (v, w)


class RedDinic:
    """
    Red con capacidades c, flujos f y listas g_mas/g_menos (vecinos salientes/entrantes).
    Se construye con (c, f) o desde un stream; después se llama a finalize() para
    precomputar adyacencias y no volver a iterar sobre todas las aristas.
    """

    FUENTE = "0"
    SUMIDERO = "1"

    def __init__(self, capacidades=None, flujos=None):
        self.c = capacidades if capacidades is not None else {}
        self.f = flujos if flujos is not None else {e: 0 for e in self.c}
        self._g_mas = None  # vértice -> lista de vértices vecinos salientes
        self._g_menos = None  # vértice -> lista de vértices vecinos entrantes

    def finalize(self):
        """Precomputa listas de adyacencia a partir de c/f. Debe llamarse antes de run."""
        self._g_mas = {}
        self._g_menos = {}
        for (v, w) in self.c:
            self._g_mas.setdefault(v, []).append(w)
            self._g_menos.setdefault(w, []).append(v)
        for v in self._g_mas:
            self._g_mas[v].sort()
        for v in self._g_menos:
            self._g_menos[v].sort()
        return self

    def vecinos_mas(self, v):
        """Vecinos salientes de v. O(1) tras finalize()."""
        return self._g_mas.get(v, ())

    def vecinos_menos(self, v):
        """Vecinos entrantes de v. O(1) tras finalize()."""
        return self._g_menos.get(v, ())

    def residual(self, v, w):
        """Capacidad residual en arista (v, w). 0 si no existe o está saturada."""
        e = arista(v, w)
        if e not in self.c:
            return 0
        return self.c[e] - self.f.get(e, 0)

    def flujo_arista(self, v, w):
        """Flujo actual en arista (v, w)."""
        return self.f.get(arista(v, w), 0)

    def aumentar_flujo(self, v, w, delta, es_backward=False):
        """Aumenta flujo en (v,w) en delta (o disminuye si es_backward en la reversa)."""
        if es_backward:
            e = arista(w, v)
            self.f[e] = self.f.get(e, 0) - delta
        else:
            e = arista(v, w)
            self.f[e] = self.f.get(e, 0) + delta

    def flujo_desde_fuente(self):
        """Valor del flujo que sale de la fuente."""
        return sum(
            self.f.get(arista(self.FUENTE, w), 0)
            for w in self.vecinos_mas(self.FUENTE)
        )
