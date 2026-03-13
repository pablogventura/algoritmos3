#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""BFS para encontrar camino aumentante en la red de flujo."""

from collections import namedtuple

from constants import FUENTE, SUMIDERO
from vertex_display import vertex_to_str

BfsElem = namedtuple("BfsElem", "vertice padre flujo esBackward")


class BFS:
    """Búsqueda en anchura desde la fuente para hallar camino al sumidero."""

    def __init__(self, matriz_cap, busqueda_normal=False):
        self.linea1 = "("
        self.linea2 = " "
        self.linea3 = " "
        self.bfs = {}
        self.llego_al_sumidero = False
        self._cap = matriz_cap
        self._cache_corte_minimal = []

        for vecino in self._cap.gamma_mas(FUENTE):
            if self._cap.no_esta_saturado(FUENTE, vecino):
                flujo = self._cap.capacidad_actual(FUENTE, vecino)
                self.bfs[vecino] = BfsElem(vecino, FUENTE, flujo, False)
                self.linea1 += ",%s    " % vertex_to_str(vecino)
                self.linea2 += ",%s    " % vertex_to_str(FUENTE)
                self.linea3 += ",%04d " % flujo

        iterador = sorted(self.bfs.keys())
        for key in iterador:
            elem = self.bfs[key]
            if busqueda_normal:
                for vecino in self._cap.gamma_mas(elem.vertice):
                    if not self._esta_en_bfs(vecino) and self._cap.no_esta_saturado(elem.vertice, vecino):
                        flujo = min(
                            self._cap.capacidad_actual(elem.vertice, vecino),
                            self._flujo_bfs(elem.vertice),
                        )
                        self.bfs[vecino] = BfsElem(vecino, elem.vertice, flujo, False)
                        self._append_lineas(vecino, elem.vertice, flujo, False)
                        iterador.append(vecino)
                        if vecino == SUMIDERO:
                            self.llego_al_sumidero = True
                            return None
                for vecino in self._cap.gamma_menos(elem.vertice):
                    if not self._esta_en_bfs(vecino) and self._cap.tiene_flujo(vecino, elem.vertice):
                        flujo = min(
                            self._cap.flujo_actual(vecino, elem.vertice),
                            self._flujo_bfs(elem.vertice),
                        )
                        self.bfs[vecino] = BfsElem(vecino, elem.vertice, flujo, True)
                        self._append_lineas(vecino, elem.vertice, flujo, True)
                        iterador.append(vecino)
            else:
                for vecino in self._cap.gamma_menos(elem.vertice):
                    if not self._esta_en_bfs(vecino) and self._cap.tiene_flujo(vecino, elem.vertice):
                        flujo = min(
                            self._cap.flujo_actual(vecino, elem.vertice),
                            self._flujo_bfs(elem.vertice),
                        )
                        self.bfs[vecino] = BfsElem(vecino, elem.vertice, flujo, True)
                        self._append_lineas(vecino, elem.vertice, flujo, True)
                        iterador.append(vecino)
                for vecino in self._cap.gamma_mas(elem.vertice):
                    if not self._esta_en_bfs(vecino) and self._cap.no_esta_saturado(elem.vertice, vecino):
                        flujo = min(
                            self._cap.capacidad_actual(elem.vertice, vecino),
                            self._flujo_bfs(elem.vertice),
                        )
                        self.bfs[vecino] = BfsElem(vecino, elem.vertice, flujo, False)
                        self._append_lineas(vecino, elem.vertice, flujo, False)
                        iterador.append(vecino)
                        if vecino == SUMIDERO:
                            self.llego_al_sumidero = True
                            return None

        if not self.llego_al_sumidero:
            self._cache_corte_minimal = [FUENTE] + list(self.bfs.keys())
        self.linea1 += ")"

    def _append_lineas(self, vecino, vertice, flujo, es_backward):
        self.linea1 += ",%s    " % vertex_to_str(vecino)
        if es_backward:
            self.linea2 += ",%s-   " % vertex_to_str(vertice)
        else:
            self.linea2 += ",%s    " % vertex_to_str(vertice)
        self.linea3 += ",%04d " % flujo

    def _flujo_bfs(self, x):
        if x == FUENTE:
            return float("inf")
        return self.bfs[x].flujo

    def devolver(self, x):
        if x == FUENTE:
            return BfsElem(FUENTE, None, float("inf"), False)
        return self.bfs[x]

    def _esta_en_bfs(self, x):
        return x == FUENTE or x in self.bfs

    def resumidero_en_bfs(self):
        if not self.llego_al_sumidero:
            return None
        return self.bfs[SUMIDERO]

    def corte_minimal(self):
        assert not self.llego_al_sumidero
        return self._cache_corte_minimal

    def __str__(self):
        return "%s\n%s\n%s" % (self.linea1, self.linea2, self.linea3)
