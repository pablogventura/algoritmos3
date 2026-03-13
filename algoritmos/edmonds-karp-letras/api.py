#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Orquestador Edmonds-Karp (versión letras) con inyección de dependencias."""

import re
from typing import Optional

from constants import VERBOSIDADES
from graph_reader import read_network
from matrizcap import MatrizCap
from bfslist import BFS
from caminoaumentante import CaminoAumentante
from output_handler import OutputHandler, VerbosityOutputHandler


class EstadoEK:
    """Orquestador del algoritmo Edmonds-Karp (entrada/salida en letras)."""

    def __init__(
        self,
        red: Optional[MatrizCap] = None,
        output: Optional[OutputHandler] = None,
        verbosidad: Optional[int] = None,
    ):
        self._cap = red if red is not None else MatrizCap()
        if output is not None:
            self._output = output
        elif verbosidad is not None:
            v = self._normalize_verbosity(verbosidad)
            self._output = VerbosityOutputHandler(v)
        else:
            self._output = VerbosityOutputHandler(0)
        self._cant_caminos = 0
        self._largo_ultimo_camino = 0
        self.flujo_maximal = 0

    def leer_un_lado(self):
        """Lee una arista desde stdin (compatibilidad). Devuelve 1 si leyó, 0 si fin."""
        try:
            entrada = input("")
        except EOFError:
            return 0
        from graph_reader import _LINEA_LETRAS, _LINEA_NUM, _token_to_vertice
        m = _LINEA_LETRAS.match(entrada.strip())
        if m:
            x = _token_to_vertice(m.group(1))
            y = _token_to_vertice(m.group(2))
            cap = int(m.group(3))
            self._cap.agregar_lado(x, y, cap)
            return 1
        m = _LINEA_NUM.match(entrada.strip())
        if m:
            x, y, cap = int(m.group(1)), int(m.group(2)), int(m.group(3))
            self._cap.agregar_lado(x, y, cap)
            return 1
        return 0

    def aumentar_flujo(self):
        """Un paso: BFS, camino aumentante, actualizar flujo. 1=ok, 0=fin, -1=error."""
        bfs = BFS(self._cap)
        if not bfs.llego_al_sumidero:
            self.flujo_maximal = self._cap.flujo_desde_fuente()
            corte = bfs.corte_minimal()
            cap_corte = self._cap.capacidad_corte(corte)
            assert cap_corte == self.flujo_maximal
            self._output.on_no_more_paths()
            self._output.on_min_cut(corte, cap_corte)
            return 0

        camino = CaminoAumentante(bfs, self._cap)
        self._cant_caminos += 1
        assert self._largo_ultimo_camino <= len(camino)
        self._largo_ultimo_camino = len(camino)

        self._output.on_augment(self._cant_caminos, camino.flujo())
        self._output.on_bfs_and_path(self._cant_caminos, str(bfs), str(camino))
        return 1

    def imprimir_flujo_maximal(self):
        red_str = str(self._cap) if self._cap.matriz else None
        self._output.on_final_flow(self.flujo_maximal, red_str)

    def run(self, stream=None):
        """Flujo completo: leer red desde stream, ejecutar algoritmo, emitir resultado."""
        red, err = read_network(stream)
        if err or red is None:
            return -1
        self._cap = red
        self._cant_caminos = 0
        self._largo_ultimo_camino = 0

        while True:
            resultado = self.aumentar_flujo()
            if resultado == 0:
                break
            if resultado == -1:
                return -1

        self.imprimir_flujo_maximal()
        return self.flujo_maximal

    @staticmethod
    def _normalize_verbosity(verbosidad):
        try:
            v = int(verbosidad)
        except (ValueError, TypeError):
            print("ERROR: La verbosidad debe ser un número.")
            print("Se asume verbosidad 0")
            return 0
        if v not in VERBOSIDADES:
            print("ERROR: Valor de verbosidad no válido.")
            print("Se asume verbosidad 0")
            return 0
        return v
