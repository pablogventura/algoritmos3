#!/usr/bin/env python3
"""Tests para códigos cíclicos (dimension, corrigeCoef, matrizGeneradora)."""
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
CICLICOS_DIR = os.path.join(REPO_ROOT, "algoritmos", "ciclicos")
CODIGOS_DIR = os.path.join(REPO_ROOT, "algoritmos", "codigos")
sys.path.insert(0, CODIGOS_DIR)
sys.path.insert(0, CICLICOS_DIR)

import ciclicos
import codigos


def test_dimension():
    # ga = 1+x+x^3, na = 7 => grado 3, dimension = 7-3 = 4
    assert ciclicos.dimension(ciclicos.ga, ciclicos.na) == 4
    assert ciclicos.dimension(ciclicos.gb, ciclicos.nb) == 4
    assert ciclicos.dimension(ciclicos.gc, ciclicos.nc) == 11  # 15 - 4


def test_corrigeCoef():
    import sympy
    x = sympy.var("x")
    p = 1 + x + x**3
    coef = ciclicos.corrigeCoef(p, 7)
    assert len(coef) == 7
    assert coef[0].valor == 1
    assert coef[1].valor == 1
    assert coef[2].valor == 0
    assert coef[3].valor == 1


def test_matrizGeneradora():
    G = ciclicos.matrizGeneradora(ciclicos.ga, ciclicos.na)
    assert G is not None
    k = ciclicos.dimension(ciclicos.ga, ciclicos.na)
    n = ciclicos.na
    # G debe ser k x n (o en la convención del código)
    import numpy
    sh = numpy.shape(G)
    assert sh[0] == k and sh[1] == n


def test_aChequeo():
    G = ciclicos.matrizGeneradora(ciclicos.ga, ciclicos.na)
    H = ciclicos.aChequeo(G)
    assert H is not None
    import numpy
    assert H.shape[1] == ciclicos.na


def run():
    ok = 0
    total = 4
    for name in ["test_dimension", "test_corrigeCoef", "test_matrizGeneradora", "test_aChequeo"]:
        try:
            globals()[name]()
            print("  OK   ciclicos %s" % name)
            ok += 1
        except Exception as e:
            print("  FAIL ciclicos %s: %s" % (name, e))
    return ok, total - ok
