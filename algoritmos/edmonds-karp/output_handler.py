#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Manejo de salida del algoritmo (Strategy): desacopla verbosidad de la lógica."""

import sys
from abc import ABC, abstractmethod

from constants import VERBOSIDADES
from vertex_display import corte_to_str


class OutputHandler(ABC):
    """Interfaz para emitir mensajes del algoritmo."""

    @abstractmethod
    def on_no_more_paths(self):
        pass

    @abstractmethod
    def on_min_cut(self, corte, capacidad):
        pass

    @abstractmethod
    def on_augment(self, paso, flujo):
        pass

    @abstractmethod
    def on_bfs_and_path(self, paso, bfs_str, camino_str):
        pass

    @abstractmethod
    def on_final_flow(self, flujo_maximal, red_str=None):
        pass


class VerbosityOutputHandler(OutputHandler):
    """Implementación que usa el nivel de verbosidad numérico."""

    def __init__(self, verbosidad=0, stream=None):
        self._v = self._normalize(verbosidad)
        self._out = stream if stream is not None else sys.stdout

    @staticmethod
    def _normalize(verbosidad):
        try:
            v = int(verbosidad)
        except (ValueError, TypeError):
            v = 0
        if v not in VERBOSIDADES:
            v = 0
        return v

    def _write(self, msg):
        self._out.write(msg + "\n")

    def on_no_more_paths(self):
        if self._v in (0, 1, 2, 10, 11, 12, 100, 101, 110, 111, 112):
            self._write("No hay mas caminos aumentantes.")

    def on_min_cut(self, corte, capacidad):
        if self._v in (100, 101, 110, 111, 112):
            self._write("Corte Minimal: S = {%s}" % corte_to_str(corte))
            self._write("Capacidad: %s" % capacidad)

    def on_augment(self, paso, flujo):
        if self._v in (1, 11, 101, 111):
            self._write("Incremento en el camino aumentante %s: %s" % (paso, flujo))

    def on_bfs_and_path(self, paso, bfs_str, camino_str):
        if self._v in (2, 12, 102, 112):
            self._write("-" * 80)
            self._write("BFS %s:" % paso)
            self._write(bfs_str)
            self._write("camino aumentante %s:" % paso)
            self._write(camino_str)

    def on_final_flow(self, flujo_maximal, red_str=None):
        if self._v in (10, 11, 12, 110, 111, 112) and red_str:
            self._write("Flujo Maximal:")
            self._write(red_str)
        self._write("Valor del flujo maximal : %s" % flujo_maximal)
