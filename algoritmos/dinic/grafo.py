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
