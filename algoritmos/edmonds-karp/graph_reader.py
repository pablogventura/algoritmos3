#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Lectura de grafo desde entrada (SRP: solo parsear y construir la red)."""

import re
import sys

from matrizcap import MatrizCap


_LINEA_ARISTA = re.compile(r"^(\d+)\s+(\d+)\s+(\d+)\s*$")


def read_network(stream=None):
    """
    Lee líneas 'x y cap' desde stream (por defecto stdin) y construye la red.
    Devuelve (MatrizCap, None) o (None, mensaje_error) si falla.
    Ordena adyacencias al final para BFS determinista y menos coste en agregar_lado.
    """
    if stream is None:
        stream = sys.stdin
    red = MatrizCap()
    try:
        for linea in stream:
            linea = linea.strip()
            if not linea:
                continue
            m = _LINEA_ARISTA.match(linea)
            if m:
                x, y, cap = int(m.group(1)), int(m.group(2)), int(m.group(3))
                red.agregar_lado(x, y, cap)
        red.finalize()
    except (ValueError, KeyError) as e:
        return None, str(e)
    return red, None
