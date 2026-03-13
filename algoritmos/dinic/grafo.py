#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Datos del grafo de ejemplo para el algoritmo de Dinic (flujo máximo)."""


def _e(*pares):
    """Convierte pares de strings en dict con claves (a,b)."""
    return {(a, b): cap for a, b, cap in pares}


def get_grafo_interno():
    """
    Devuelve (capacidades, flujos) del grafo interno.
    Los flujos se devuelven como copia inicializada en 0.
    """
    c = _e(
        ("0", "A", 144), ("0", "B", 96), ("0", "N", 150),
        ("A", "C", 100), ("A", "D", 70), ("A", "F", 85), ("A", "L", 17),
        ("B", "C", 10), ("B", "D", 17), ("B", "G", 102), ("B", "L", 35),
        ("C", "1", 80), ("C", "J", 5), ("D", "1", 80),
        ("E", "C", 100), ("E", "D", 15), ("E", "G", 10),
        ("F", "H", 15), ("F", "K", 100), ("G", "1", 80), ("H", "1", 20), ("H", "M", 40),
        ("I", "D", 22), ("I", "G", 10), ("J", "A", 5), ("K", "1", 120),
        ("L", "H", 30), ("L", "K", 60), ("M", "1", 30),
        ("N", "E", 110), ("N", "I", 40),
    )
    f = {arista: 0 for arista in c}
    return c, f


def get_grafo_n2():
    """Grafo n2 (practico4); flujo esperado: 37."""
    c = _e(
        ("0", "A", 15), ("0", "D", 20), ("0", "J", 7),
        ("A", "B", 17), ("A", "H", 5), ("B", "C", 15), ("C", "1", 20),
        ("D", "C", 26), ("D", "E", 5), ("D", "G", 10), ("D", "I", 6),
        ("E", "F", 5), ("E", "K", 2), ("F", "1", 5),
        ("G", "K", 10), ("G", "M", 3), ("G", "O", 1),
        ("H", "N", 4), ("I", "F", 4), ("J", "L", 7), ("K", "1", 10),
        ("L", "B", 5), ("L", "N", 4), ("M", "1", 1), ("N", "C", 6), ("O", "1", 10),
    )
    f = {arista: 0 for arista in c}
    return c, f


def get_grafo_n3():
    """Grafo n3 (practico4); flujo esperado: 108."""
    c = _e(
        ("0", "A", 20), ("0", "B", 69), ("0", "C", 145),
        ("A", "D", 14), ("A", "E", 19), ("A", "F", 18),
        ("B", "D", 9), ("B", "E", 4), ("B", "F", 14), ("B", "H", 1),
        ("C", "E", 190), ("C", "F", 4), ("C", "H", 20), ("C", "I", 20),
        ("D", "1", 9), ("D", "H", 8), ("D", "I", 1), ("D", "J", 7),
        ("E", "1", 16), ("E", "H", 2), ("E", "I", 16), ("E", "J", 7),
        ("F", "1", 146), ("G", "I", 5), ("H", "1", 25), ("I", "1", 15), ("J", "1", 7),
    )
    f = {arista: 0 for arista in c}
    return c, f


def get_grafo_n4():
    """Grafo n4 (practico4); flujo esperado: 300."""
    c = _e(
        ("0", "U", 160), ("0", "V", 50), ("0", "W", 100),
        ("A", "H", 20), ("A", "N", 10), ("B", "H", 10), ("B", "I", 20),
        ("C", "I", 10), ("C", "J", 20), ("D", "J", 15), ("D", "K", 20),
        ("E", "K", 15), ("E", "L", 20), ("F", "L", 15), ("F", "M", 20),
        ("G", "M", 15), ("G", "N", 10),
        ("H", "1", 20), ("I", "1", 20), ("J", "1", 20), ("K", "1", 20), ("L", "1", 20), ("M", "1", 20), ("N", "1", 20),
        ("P", "A", 20), ("P", "B", 20), ("P", "C", 20), ("P", "D", 20), ("P", "E", 20), ("P", "F", 20), ("P", "G", 25),
        ("Q", "X", 50), ("Q", "Z", 50), ("R", "X", 50), ("R", "Z", 50),
        ("U", "X", 60), ("U", "Y", 200), ("U", "Z", 100),
        ("V", "Q", 70), ("V", "R", 20), ("W", "Q", 70), ("W", "R", 30),
        ("X", "1", 60), ("Y", "P", 200), ("Z", "1", 100),
    )
    f = {arista: 0 for arista in c}
    return c, f
