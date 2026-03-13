#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Camino aumentante desde la fuente al sumidero."""

from collections import namedtuple

from constants import FUENTE, SUMIDERO
from vertex_display import vertex_to_str

CAElem = namedtuple("CAElem", "vertice esBackward")


class CaminoAumentante:
    """Camino aumentante construido a partir del BFS."""

    def __init__(self, bfs, matriz_cap):
        self._camino = []
        self.bfs = bfs
        self._cap = matriz_cap

        aux = self.bfs.resumidero_en_bfs()
        if aux is None:
            return
        self._flujo = aux.flujo
        self._camino.append(CAElem(aux.vertice, aux.esBackward))

        while aux.vertice != FUENTE:
            if aux.esBackward:
                self._cap.flujo_backward(aux.padre, aux.vertice, self._flujo)
            else:
                self._cap.flujo_forward(aux.padre, aux.vertice, self._flujo)
            aux = self.bfs.devolver(aux.padre)
            self._camino.append(CAElem(aux.vertice, aux.esBackward))

        self._camino.reverse()

    def __len__(self):
        return len(self._camino)

    def flujo(self):
        return self._flujo

    def __str__(self):
        partes = []
        for (vertice, es_backward) in self._camino:
            s = vertex_to_str(vertice)
            partes.append("<" + s if es_backward else "," + s)
        return "".join(partes)[1:] + ": " + str(self._flujo)
