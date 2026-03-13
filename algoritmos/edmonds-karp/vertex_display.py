#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Formateo de vértices para salida (fuente, sumidero, otros)."""

from constants import FUENTE, SUMIDERO


def vertex_to_str(vertice):
    """Convierte id de vértice a string para mostrar (s/t o número/carácter)."""
    if vertice == FUENTE:
        return "s"
    if vertice == SUMIDERO:
        return "t"
    if 0 <= vertice <= 0x10FFFF:
        return chr(vertice)
    return str(vertice)


def corte_to_str(corte):
    """Convierte una lista de vértices (corte) a string para mostrar."""
    return ", ".join(vertex_to_str(v) for v in corte)
