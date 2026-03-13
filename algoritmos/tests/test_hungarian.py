#!/usr/bin/env python3
"""Tests para el algoritmo húngaro (asignación de costo mínimo)."""
import os
import sys
import io

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
HUNG_DIR = os.path.join(REPO_ROOT, "algoritmos", "hungarian")
sys.path.insert(0, HUNG_DIR)

# Redirigir stdout para no imprimir "Costo Total:..." en cada test
import hung


def test_hungaro_2x2():
    # Matriz [[1,2],[3,4]]: asignación óptima (0,0)+(1,1) = 1+4 = 5 o (0,1)+(1,0) = 2+3 = 5
    mat = [[1, 2], [3, 4]]
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        matching, _ = hung.hungaro(mat)
    finally:
        sys.stdout = old
    cost = sum(matching[k] for k in matching)
    assert cost == 5
    assert len(matching) == 2


def test_hungaro_3x3():
    # Matriz: mínimo 1+1+1 = 3 (filas 0->col1, 1->col2, 2->col0)
    mat = [[3, 1, 2], [2, 4, 1], [1, 2, 3]]
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        matching, _ = hung.hungaro(mat)
    finally:
        sys.stdout = old
    cost = sum(matching[k] for k in matching)
    assert cost == 3
    assert len(matching) == 3


def test_hungaro_diagonal():
    # 1 en diagonal, 0 fuera: asignación óptima usa los 0 → costo 0
    mat = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    old = sys.stdout
    sys.stdout = io.StringIO()
    try:
        matching, _ = hung.hungaro(mat)
    finally:
        sys.stdout = old
    cost = sum(matching[k] for k in matching)
    assert cost == 0
    assert len(matching) == 3


def run():
    ok = 0
    total = 3
    for name in ["test_hungaro_2x2", "test_hungaro_3x3", "test_hungaro_diagonal"]:
        try:
            globals()[name]()
            print("  OK   hungarian %s" % name)
            ok += 1
        except Exception as e:
            print("  FAIL hungarian %s: %s" % (name, e))
    return ok, total - ok
