#!/usr/bin/env python3
"""Tests para codigos (Z₂, recorre, identidad, w) y generacodigos."""
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
CODIGOS_DIR = os.path.join(REPO_ROOT, "algoritmos", "codigos")
sys.path.insert(0, CODIGOS_DIR)

import codigos
import generacodigos as gen


def test_z2():
    assert codigos.z2(0).valor == 0
    assert codigos.z2(1).valor == 1
    assert codigos.z2(0) + codigos.z2(1) == codigos.z2(1)
    assert codigos.z2(1) + codigos.z2(1) == codigos.z2(0)
    assert codigos.z2(2).valor == 0


def test_recorre():
    r0 = codigos.recorre(0)
    assert r0 == [""]
    r2 = codigos.recorre(2)
    assert set(r2) == {"00", "01", "10", "11"}
    assert len(codigos.recorre(3)) == 8


def test_identidad():
    I = codigos.identidad(2)
    assert I.shape == (2, 2)
    assert I[0, 0].valor == 1 and I[0, 1].valor == 0
    assert I[1, 0].valor == 0 and I[1, 1].valor == 1


def test_w():
    # w(palabra) = peso (cantidad de 1s). Construir fila explícita de z2 para evitar dependencia de g3
    import numpy
    fila = [[codigos.z2(1), codigos.z2(0), codigos.z2(1), codigos.z2(1), codigos.z2(0)]]
    pal = numpy.matrix(fila)
    assert codigos.w(pal) == 3


def test_resuelve():
    assert gen.resuelve(lambda x: x * x, 10) == 4
    assert gen.resuelve(lambda x: 2 ** x, 8) == 3


def test_todascolumnas():
    # k=2, n tal que 2^n - 1 - n >= 2
    cols = gen.todascolumnas(2, 3)
    assert cols is not None
    import numpy
    assert cols.shape[0] == 3


def test_generaChequeoCodigo():
    H = gen.generaChequeoCodigo(8)
    assert H is not None
    import numpy
    assert H.shape[0] >= 3


def run():
    ok = 0
    total = 7
    for name in ["test_z2", "test_recorre", "test_identidad", "test_w", "test_resuelve", "test_todascolumnas", "test_generaChequeoCodigo"]:
        try:
            globals()[name]()
            print("  OK   codigos %s" % name)
            ok += 1
        except Exception as e:
            print("  FAIL codigos %s: %s" % (name, e))
    return ok, total - ok
