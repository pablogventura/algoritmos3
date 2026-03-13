#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Algoritmo de Dinic para flujo máximo.
Red inyectable (capacidades c, flujos f) y salida inyectable (stream).
Con --stdin lee líneas "x y cap" por stdin (fuente 0, sumidero 1) e imprime el flujo maximal.
"""

import argparse
import sys


def _arista(v, w):
    """Clave de arista: (v,w) para soportar vértices con id de cualquier longitud."""
    return (v, w)


def vecinos_mas(v, red):
    """Vecinos salientes de v en la red (red: dict con claves (a,b))."""
    result = [b for (a, b) in red if a == v]
    result.sort()
    return result


def vecinos_menos(v, red):
    """Vecinos entrantes de v en la red."""
    result = [a for (a, b) in red if b == v]
    result.sort()
    return result


def red_residual(c, f):
    """BFS: construye la red residual (niveles) desde fuente '0' hacia '1'."""
    result = {}
    q = []
    visitado = {}
    q.append("0")
    visitado["0"] = 0

    while q:
        v = q.pop(0)
        for w in vecinos_mas(v, c):
            if "1" not in visitado or w == "1":
                arista = _arista(v, w)
                if arista in c and (w not in visitado or visitado[w] == visitado[v] + 1):
                    if c[arista] - f[arista] > 0:
                        visitado[w] = visitado[v] + 1
                        q.append(w)
                        result[arista] = (c[arista] - f[arista], False)
        for w in vecinos_menos(v, c):
            if "1" not in visitado or w == "1":
                arista_rev = _arista(w, v)
                if arista_rev in f and (w not in visitado or visitado[w] == visitado[v] + 1):
                    if f[arista_rev] > 0:
                        visitado[w] = visitado[v] + 1
                        q.append(w)
                        result[_arista(v, w)] = (f[arista_rev], True)

    return result


def camino_dfs(na, c, f):
    """DFS desde '0' a '1' en la red residual na; devuelve un camino (dict) o vacío."""
    s = []
    visitado = []
    s.append("0")
    visitado.append("0")
    result = {}

    while s:
        v = s[-1]
        agrego = False
        for w in vecinos_mas(v, na):
            if w not in visitado:
                agrego = True
                visitado.append(w)
                s.append(w)
                arista = _arista(v, w)
                if not na[arista][1]:
                    result[arista] = (c[arista] - f[arista], False)
                else:
                    result[arista] = (f[_arista(w, v)], True)
                if w == "1":
                    return result
                break
        if not agrego:
            for w in vecinos_mas(v, result):
                del result[_arista(v, w)]
            for w in vecinos_menos(v, result):
                del result[_arista(w, v)]
            del s[-1]

    return result


def formato_camino(camino):
    """Formatea un camino (dict arista -> (cap_residual, es_backward)) como string."""
    if not camino:
        return ""
    fc = min(camino[vw][0] for vw in camino)
    v = "0"
    result = v
    w_list = vecinos_mas(v, camino)
    while w_list:
        assert len(w_list) == 1
        w = w_list[0]
        arista = _arista(v, w)
        if not camino[arista][1]:
            result += "," + w
        else:
            result += "<" + w
        v = w
        w_list = vecinos_mas(w, camino)
    result += ":%s" % fc
    return result


def actualizar_flujo(na, camino, f):
    """Actualiza el flujo f a lo largo del camino en la red residual na."""
    fc = min(camino[vw][0] for vw in camino)
    for arista in camino:
        v, w = arista[0], arista[1]
        if not camino[arista][1]:
            f[arista] = f.get(arista, 0) + fc
            na[arista] = (na[arista][0] - fc, na[arista][1])
            if na[arista][0] == 0:
                del na[arista]
        else:
            rev = _arista(w, v)
            f[rev] = f.get(rev, 0) - fc
            na[arista] = (na[arista][0] - fc, na[arista][1])
            if na[arista][0] == 0:
                del na[arista]


def run(capacidades, flujos, output_stream=None, solo_valor=False):
    """
    Ejecuta Dinic sobre la red (capacidades, flujos).
    Escribe los caminos y el valor del flujo maximal en output_stream.
    Si solo_valor es True, solo escribe la línea del flujo maximal (para tests).
    Devuelve el valor del flujo maximal.
    """
    if output_stream is None:
        output_stream = sys.stdout
    c = capacidades
    f = flujos
    caminos_str = []
    aux = red_residual(c, f)
    while "1" in [b for (_, b) in aux]:
        camino = camino_dfs(aux, c, f)
        while "1" in [b for (_, b) in camino]:
            caminos_str.append(formato_camino(camino))
            actualizar_flujo(aux, camino, f)
            camino = camino_dfs(aux, c, f)
        aux = red_residual(c, f)
    if not solo_valor:
        for linea in caminos_str:
            output_stream.write(linea + "\n")
    total = sum(f[k] for k in f if k[0] == "0")
    output_stream.write("Valor del flujo maximal : %s\n" % total)
    return total


def grafo_desde_stdin(stream):
    """Lee líneas 'x y cap' del stream y devuelve (c, f) con claves de arista (str(x), str(y))."""
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
        arista = _arista(x, y)
        c[arista] = cap
    f = {arista: 0 for arista in c}
    return c, f


def main():
    """Punto de entrada: grafo interno o --stdin (x y cap por stdin)."""
    parser = argparse.ArgumentParser(description="Dinic: flujo máximo")
    parser.add_argument("--stdin", action="store_true", help="Leer red por stdin (líneas 'x y cap'); fuente 0, sumidero 1")
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
