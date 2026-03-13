#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Lectura de grafo desde entrada: acepta líneas numéricas (x y cap) o letras (A B cap)."""

import re
import sys

from matrizcap import MatrizCap


_LINEA_NUM = re.compile(r"^(\d+)\s+(\d+)\s+(\d+)\s*$")
_LINEA_LETRAS = re.compile(r"^([a-zA-Z])\s+([a-zA-Z])\s+(\d+)\s*$")


def _token_to_vertice(s):
    """Convierte token 's'/'t'/letra o número a id de vértice."""
    if s in ("s", "S"):
        return 0
    if s in ("t", "T"):
        return 1
    if len(s) == 1:
        return ord(s)
    return int(s)


def read_network(stream=None):
    """
    Lee líneas 'x y cap' (números o letras) desde stream (por defecto stdin).
    Devuelve (MatrizCap, None) o (None, mensaje_error).
    """
    if stream is None:
        stream = sys.stdin
    red = MatrizCap()
    try:
        for linea in stream:
            linea = linea.strip()
            if not linea:
                continue
            m = _LINEA_LETRAS.match(linea)
            if m:
                x = _token_to_vertice(m.group(1))
                y = _token_to_vertice(m.group(2))
                cap = int(m.group(3))
                red.agregar_lado(x, y, cap)
                continue
            m = _LINEA_NUM.match(linea)
            if m:
                x, y, cap = int(m.group(1)), int(m.group(2)), int(m.group(3))
                red.agregar_lado(x, y, cap)
        red.finalize()
    except (ValueError, KeyError) as e:
        return None, str(e)
    return red, None
