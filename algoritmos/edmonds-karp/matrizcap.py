#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Matriz de capacidades y flujo para la red (grafo con capacidades)."""

from constants import FUENTE, SUMIDERO
from vertex_display import vertex_to_str


class MatrizCap:
    """
    Red como matriz de capacidades y flujo actual por arista.
    Tras agregar todos los lados, llamar a finalize() para ordenar adyacencias (opcional pero recomendado).
    """

    def __init__(self):
        self.matriz = {}
        self.g_mas = {}
        self.g_menos = {}
        self._cache_flujo_desde_fuente = 0
        self._finalized = False

    def agregar_lado(self, x, y, cap):
        """Agrega la arista (x, y) con capacidad cap; flujo inicial 0."""
        self.matriz[(x, y)] = (cap, 0)
        self.g_mas.setdefault(x, []).append(y)
        self.g_menos.setdefault(y, []).append(x)
        self._finalized = False

    def finalize(self):
        """Ordena listas de adyacencia una sola vez. Llamar tras terminar de agregar lados."""
        if self._finalized:
            return
        for v in self.g_mas:
            self.g_mas[v].sort()
        for v in self.g_menos:
            self.g_menos[v].sort()
        self._finalized = True

    def capacidad_total(self, x, y):
        """Capacidad total del lado (x, y)."""
        return self.matriz[(x, y)][0]

    def flujo_actual(self, x, y):
        """Flujo actual del lado (x, y)."""
        return self.matriz[(x, y)][1]

    def capacidad_actual(self, x, y):
        """Capacidad residual del lado (x, y)."""
        return self.capacidad_total(x, y) - self.flujo_actual(x, y)

    def gamma_mas(self, x):
        """Vecinos salientes del vértice x."""
        return self.g_mas.get(x, [])

    def gamma_menos(self, x):
        """Vecinos entrantes del vértice x."""
        return self.g_menos.get(x, [])

    def no_esta_saturado(self, x, y):
        """True si el lado (x, y) tiene capacidad residual."""
        return self.capacidad_actual(x, y) > 0

    def tiene_flujo(self, x, y):
        """True si el lado (x, y) tiene flujo positivo."""
        return self.flujo_actual(x, y) > 0

    def flujo_desde_fuente(self):
        """Valor del flujo que sale de la fuente (flujo maximal al terminar)."""
        return self._cache_flujo_desde_fuente

    def flujo_forward(self, x, y, flujo):
        """Aumenta el flujo en la arista (x, y) en flujo."""
        cap, actual = self.matriz[(x, y)]
        self.matriz[(x, y)] = (cap, actual + flujo)
        if x == FUENTE:
            self._cache_flujo_desde_fuente += flujo

    def flujo_backward(self, x, y, flujo):
        """Reduce el flujo en la arista (y, x) en flujo (retroceso)."""
        cap, actual = self.matriz[(y, x)]
        self.matriz[(y, x)] = (cap, actual - flujo)
        if x == FUENTE:
            self._cache_flujo_desde_fuente -= flujo

    def capacidad_corte(self, corte):
        """Capacidad del corte (conjunto de vértices S)."""
        cap_corte = 0
        for elem in corte:
            for hijo in self.gamma_mas(elem):
                if hijo not in corte and self.capacidad_actual(elem, hijo) == 0:
                    cap_corte += self.capacidad_total(elem, hijo)
        return cap_corte

    def __str__(self):
        """Representación en texto de la matriz de flujo."""
        lineas = []
        for (x, y) in sorted(self.matriz.keys()):
            flujo = self.matriz[(x, y)][1]
            xs = vertex_to_str(x)
            ys = vertex_to_str(y)
            lineas.append("Lado %s,%s: %s" % (xs, ys, flujo))
        return "\n".join(lineas)
