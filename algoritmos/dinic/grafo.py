#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Datos del grafo de ejemplo para el algoritmo de Dinic (flujo máximo)."""


def get_grafo_interno():
    """
    Devuelve (capacidades, flujos) del grafo interno.
    Los flujos se devuelven como copia inicializada en 0.
    """
    c = {
        "0A": 144, "0B": 96, "0N": 150,
        "AC": 100, "AD": 70, "AF": 85, "AL": 17,
        "BC": 10, "BD": 17, "BG": 102, "BL": 35,
        "C1": 80, "CJ": 5, "D1": 80,
        "EC": 100, "ED": 15, "EG": 10,
        "FH": 15, "FK": 100, "G1": 80, "H1": 20, "HM": 40,
        "ID": 22, "IG": 10, "JA": 5, "K1": 120,
        "LH": 30, "LK": 60, "M1": 30,
        "NE": 110, "NI": 40,
    }
    f = {arista: 0 for arista in c}
    return c, f


def get_grafo_n2():
    """Grafo n2 (practico4); flujo esperado: 37."""
    c = {
        "0A": 15, "0D": 20, "0J": 7,
        "AB": 17, "AH": 5, "BC": 15, "C1": 20,
        "DC": 26, "DE": 5, "DG": 10, "DI": 6,
        "EF": 5, "EK": 2, "F1": 5,
        "GK": 10, "GM": 3, "GO": 1,
        "HN": 4, "IF": 4, "JL": 7, "K1": 10,
        "LB": 5, "LN": 4, "M1": 1, "NC": 6, "O1": 10,
    }
    f = {arista: 0 for arista in c}
    return c, f


def get_grafo_n3():
    """Grafo n3 (practico4); flujo esperado: 108."""
    c = {
        "0A": 20, "0B": 69, "0C": 145,
        "AD": 14, "AE": 19, "AF": 18,
        "BD": 9, "BE": 4, "BF": 14, "BH": 1,
        "CE": 190, "CF": 4, "CH": 20, "CI": 20,
        "D1": 9, "DH": 8, "DI": 1, "DJ": 7,
        "E1": 16, "EH": 2, "EI": 16, "EJ": 7,
        "F1": 146, "GI": 5, "H1": 25, "I1": 15, "J1": 7,
    }
    f = {arista: 0 for arista in c}
    return c, f


def get_grafo_n4():
    """Grafo n4 (practico4); flujo esperado: 300."""
    c = {
        "0U": 160, "0V": 50, "0W": 100,
        "AH": 20, "AN": 10, "BH": 10, "BI": 20,
        "CI": 10, "CJ": 20, "DJ": 15, "DK": 20,
        "EK": 15, "EL": 20, "FL": 15, "FM": 20,
        "GM": 15, "GN": 10,
        "H1": 20, "I1": 20, "J1": 20, "K1": 20, "L1": 20, "M1": 20, "N1": 20,
        "PA": 20, "PB": 20, "PC": 20, "PD": 20, "PE": 20, "PF": 20, "PG": 25,
        "QX": 50, "QZ": 50, "RX": 50, "RZ": 50,
        "UX": 60, "UY": 200, "UZ": 100,
        "VQ": 70, "VR": 20, "WQ": 70, "WR": 30,
        "X1": 60, "YP": 200, "Z1": 100,
    }
    f = {arista: 0 for arista in c}
    return c, f
