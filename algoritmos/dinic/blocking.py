#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Flujo bloqueante (Dinic): DFS desde la fuente al sumidero en el grafo de niveles.
Usa "current arc" (índice por vértice) para no reescanear aristas ya agotadas.
"""

from red import RedDinic, arista


class EstadoBlocking:
    """Índice de la siguiente arista a probar por vértice (current arc)."""

    def __init__(self, red):
        self._i_fwd = {v: 0 for v in red._g_mas or {}}
        self._i_bwd = {v: 0 for v in red._g_menos or {}}

    def reset(self, red):
        for v in red._g_mas or {}:
            self._i_fwd[v] = 0
        for v in red._g_menos or {}:
            self._i_bwd[v] = 0


def _dfs(red, nivel, estado, v, flujo_entrante):
    """
    DFS desde v hacia el sumidero en el grafo de niveles.
    Devuelve flujo enviado (0 si no hay camino).
    """
    if v == red.SUMIDERO:
        return flujo_entrante

    lv = nivel.get(v, -1)
    vecinos_mas = red.vecinos_mas(v)
    vecinos_menos = red.vecinos_menos(v)
    i_fwd = estado._i_fwd
    i_bwd = estado._i_bwd

    # Aristas salientes
    while i_fwd.get(v, 0) < len(vecinos_mas):
        idx = i_fwd.get(v, 0)
        w = vecinos_mas[idx]
        i_fwd[v] = idx + 1
        if nivel.get(w, -1) != lv + 1:
            continue
        res = red.residual(v, w)
        if res <= 0:
            continue
        env = min(flujo_entrante, res)
        got = _dfs(red, nivel, estado, w, env)
        if got > 0:
            red.aumentar_flujo(v, w, got, es_backward=False)
            return got

    # Aristas entrantes (reversa)
    while i_bwd.get(v, 0) < len(vecinos_menos):
        idx = i_bwd.get(v, 0)
        u = vecinos_menos[idx]
        i_bwd[v] = idx + 1
        if nivel.get(u, -1) != lv + 1:
            continue
        fl = red.flujo_arista(u, v)
        if fl <= 0:
            continue
        env = min(flujo_entrante, fl)
        got = _dfs(red, nivel, estado, u, env)
        if got > 0:
            red.aumentar_flujo(u, v, got, es_backward=True)
            return got

    return 0


def flujo_bloqueante(red, nivel, estado):
    """
    Una fase de flujo bloqueante: repetir DFS hasta agotar caminos.
    Devuelve el flujo total enviado en esta fase.
    """
    estado.reset(red)
    total = 0
    while True:
        flujo = _dfs(red, nivel, estado, red.FUENTE, float("inf"))
        if flujo == 0:
            break
        total += flujo
    return total
