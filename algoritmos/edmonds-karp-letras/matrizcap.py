#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Matriz de capacidades y flujo para la red (versión letras)."""

from constants import FUENTE, SUMIDERO
from vertex_display import vertex_to_str


class MatrizCap:
    """Red como matriz de capacidades y flujo actual por arista."""

    def __init__(self):
        self.matriz = {}
        self.g_mas = {}
        self.g_menos = {}
        self._cache_flujo_desde_fuente = 0

    def agregar_lado(self, x, y, cap):
        """Agrega la arista (x, y) con capacidad cap; flujo inicial 0."""
        self.matriz[(x, y)] = (cap, 0)
        if x not in self.g_mas:
            self.g_mas[x] = []
        self.g_mas[x].append(y)
        self.g_mas[x].sort()
        if y not in self.g_menos:
            self.g_menos[y] = []
        self.g_menos[y].append(x)
        self.g_menos[y].sort()

    def capacidad_total(self, x, y):
        return self.matriz[(x, y)][0]

    def flujo_actual(self, x, y):
        return self.matriz[(x, y)][1]

    def capacidad_actual(self, x, y):
        return self.capacidad_total(x, y) - self.flujo_actual(x, y)

    def gamma_mas(self, x):
        return self.g_mas.get(x, [])

    def gamma_menos(self, x):
        return self.g_menos.get(x, [])

    def no_esta_saturado(self, x, y):
        return self.capacidad_actual(x, y) > 0

    def tiene_flujo(self, x, y):
        return self.flujo_actual(x, y) > 0

    def flujo_desde_fuente(self):
        return self._cache_flujo_desde_fuente

    def flujo_forward(self, x, y, flujo):
        cap, actual = self.matriz[(x, y)]
        self.matriz[(x, y)] = (cap, actual + flujo)
        if x == FUENTE:
            self._cache_flujo_desde_fuente += flujo

    def flujo_backward(self, x, y, flujo):
        cap, actual = self.matriz[(y, x)]
        self.matriz[(y, x)] = (cap, actual - flujo)
        if x == FUENTE:
            self._cache_flujo_desde_fuente -= flujo

    def capacidad_corte(self, corte):
        cap_corte = 0
        for elem in corte:
            for hijo in self.gamma_mas(elem):
                if hijo not in corte and self.capacidad_actual(elem, hijo) == 0:
                    cap_corte += self.capacidad_total(elem, hijo)
        return cap_corte

    def __str__(self):
        lineas = []
        for (x, y) in sorted(self.matriz.keys()):
            flujo = self.matriz[(x, y)][1]
            lineas.append("Lado %s,%s: %s" % (vertex_to_str(x), vertex_to_str(y), flujo))
        return "\n".join(lineas)
