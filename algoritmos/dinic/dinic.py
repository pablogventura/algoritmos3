#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Algoritmo de Dinic para flujo máximo.
Modular: red (red.py), BFS de niveles (niveles.py), flujo bloqueante (blocking.py).
Con --stdin lee líneas "x y cap" por stdin (fuente 0, sumidero 1).
"""

import argparse
import sys

from red import RedDinic, arista
from niveles import bfs_niveles
from blocking import flujo_bloqueante, EstadoBlocking


def run(capacidades, flujos, output_stream=None, solo_valor=False):
    """
    Ejecuta Dinic sobre la red (capacidades, flujos).
    capacidades y flujos: dict con claves (v, w) — vértices como str.
    Si solo_valor es True, solo escribe la línea del flujo maximal (para tests).
    Devuelve el valor del flujo maximal.
    """
    if output_stream is None:
        output_stream = sys.stdout
    red = RedDinic(capacidades, flujos)
    red.finalize()
    estado = EstadoBlocking(red)

    while True:
        nivel = bfs_niveles(red)
        if nivel is None:
            break
        flujo_bloqueante(red, nivel, estado)

    total = red.flujo_desde_fuente()
    output_stream.write("Valor del flujo maximal : %s\n" % total)
    return total


def grafo_desde_stdin(stream):
    """Lee líneas 'x y cap' del stream. Devuelve (c, f) con claves (str, str)."""
    c = {}
    for line in stream:
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) != 3:
            continue
        try:
            x, y, cap = str(parts[0]), str(parts[1]), int(parts[2])
        except ValueError:
            continue
        c[arista(x, y)] = cap
    f = {e: 0 for e in c}
    return c, f


def main():
    """Punto de entrada: grafo interno o --stdin (x y cap por stdin)."""
    parser = argparse.ArgumentParser(description="Dinic: flujo máximo")
    parser.add_argument(
        "--stdin",
        action="store_true",
        help="Leer red por stdin (líneas 'x y cap'); fuente 0, sumidero 1",
    )
    args = parser.parse_args()
    if args.stdin:
        c, f = grafo_desde_stdin(sys.stdin)
        run(c, f, sys.stdout, solo_valor=True)
    else:
        from grafo import get_grafo_interno
        c, f = get_grafo_interno()
        run(c, f, sys.stdout)


if __name__ == "__main__":
    main()
