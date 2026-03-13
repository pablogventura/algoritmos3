#!/usr/bin/env python3
"""Tests para coloreo (heurísticas greedy, DSatur, etc.)."""
import os
import sys
import io

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
COLOREO_DIR = os.path.join(REPO_ROOT, "algoritmos", "coloreo")
sys.path.insert(0, COLOREO_DIR)

import heuristicas as h
import probando


def _es_coloreo_valido(grafo, coloreo):
    for v in grafo:
        if v not in coloreo:
            return False
        for w in grafo[v]:
            if w in coloreo and coloreo[v] == coloreo[w]:
                return False
    return True


def test_greedy_grafo_chico():
    grafo = {"a": ["b"], "b": ["a"]}
    orden = ["a", "b"]
    col = h.greedy(grafo, orden)
    assert _es_coloreo_valido(grafo, col)
    assert set(col.keys()) == set(grafo.keys())
    assert len(set(col.values())) == 2


def test_greedy_grafo_g1():
    grafo = probando.g1
    orden = h.ordena(list(grafo.keys()), grafo)
    col = h.greedy(grafo, orden)
    assert _es_coloreo_valido(grafo, col)
    assert set(col.keys()) == set(grafo.keys())


def test_dsatur_grafo_chico():
    grafo = {"a": ["b", "c"], "b": ["a", "c"], "c": ["a", "b"]}
    out = io.StringIO()
    old = sys.stdout
    sys.stdout = out
    try:
        col = h.dsatur(grafo)
    finally:
        sys.stdout = old
    assert _es_coloreo_valido(grafo, col)
    assert set(col.keys()) == set(grafo.keys())
    assert len(set(col.values())) == 3


def test_paso_greedy():
    grafo = {"a": ["b"], "b": ["a"]}
    col = {}
    c1 = h.paso_greedy(grafo, col, "a")
    assert c1 == 1
    col["a"] = 1
    c2 = h.paso_greedy(grafo, col, "b")
    assert c2 == 2


def run():
    ok = 0
    total = 4
    for name in ["test_greedy_grafo_chico", "test_greedy_grafo_g1", "test_dsatur_grafo_chico", "test_paso_greedy"]:
        try:
            globals()[name]()
            print("  OK   coloreo %s" % name)
            ok += 1
        except Exception as e:
            print("  FAIL coloreo %s: %s" % (name, e))
    return ok, total - ok
