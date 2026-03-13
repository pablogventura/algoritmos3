#!/usr/bin/env python3
"""Tests para el módulo corte (corte mínimo en red de flujo)."""
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
CORTE_DIR = os.path.join(REPO_ROOT, "algoritmos", "corte")
sys.path.insert(0, CORTE_DIR)

import networkcorte as corte


def test_ntog():
    g, c = corte.ntog(corte.n)
    assert "s" in g
    assert "t" in g
    assert ("s", "a") in c
    assert c[("s", "a")] == 4
    assert ("b", "t") in c


def test_corteminimal():
    s = corte.corteminimal(corte.n, corte.f)
    assert "s" in s
    assert "t" not in s
    assert isinstance(s, list)
    # En el ejemplo, el corte mínimo deja s,a,c de un lado (alcanzables desde s en residual)
    assert "a" in s or "c" in s


def test_capacidadCorte():
    s = corte.corteminimal(corte.n, corte.f)
    cap = corte.capacidadCorte(s, corte.n, corte.f)
    # Flujo que cruza el corte (S -> T) para este f y S
    assert cap > 0
    assert isinstance(cap, (int, float))


def test_valorFlujo():
    val = corte.valorFlujo(corte.f, corte.n)
    # Flujo que entra en t en el ejemplo es 4+2 = 6
    assert val == 6


def run():
    ok = 0
    for name in ["test_ntog", "test_corteminimal", "test_capacidadCorte", "test_valorFlujo"]:
        try:
            globals()[name]()
            print("  OK   corte %s" % name)
            ok += 1
        except Exception as e:
            print("  FAIL corte %s: %s" % (name, e))
    return ok, 4 - ok
