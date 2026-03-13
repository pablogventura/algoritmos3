#!/usr/bin/env python3
"""
Tests de Dinic con varios grafos (n1, n2, n3, n4) provenientes de practicos.
Ejecutar desde repo root: python3 algoritmos/tests/test_dinic_grafos.py
"""
import io
import os
import sys

# Permitir importar dinic y grafo
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
DINIC_DIR = os.path.abspath(os.path.join(TESTS_DIR, "..", "dinic"))
sys.path.insert(0, DINIC_DIR)

import dinic
import grafo

ESPERADOS = {"n2": 37, "n3": 108, "n4": 300}


def main():
    ok = 0
    fail = 0
    # n1 se prueba como "grafo interno" en run_tests; aquí solo n2, n3, n4
    for name, getter in [
        ("n2", grafo.get_grafo_n2),
        ("n3", grafo.get_grafo_n3),
        ("n4", grafo.get_grafo_n4),
    ]:
        c, f = getter()
        out = io.StringIO()
        total = dinic.run(c, f, out)
        esperado = ESPERADOS[name]
        if total == esperado:
            print("  OK   dinic %s (flujo %s)" % (name, total))
            ok += 1
        else:
            print("  FAIL dinic %s: esperado %s, obtuvo %s" % (name, esperado, total))
            fail += 1
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
