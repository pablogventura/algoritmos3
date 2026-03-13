#!/usr/bin/env python3
"""
Ejecuta los tests de los algoritmos que no son flujo máximo: corte, wave, coloreo,
codigos, ciclicos, hungarian.

Uso (desde la raíz del repo o desde algoritmos/tests):
  python3 run_tests_otros.py
  python3 run_tests_otros.py --impl corte
  python3 run_tests_otros.py --list
"""
import argparse
import os
import sys

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))

MODULOS = {
    "corte": "test_corte",
    "wave": "test_wave",
    "coloreo": "test_coloreo",
    "codigos": "test_codigos",
    "ciclicos": "test_ciclicos",
    "hungarian": "test_hungarian",
}


def main():
    parser = argparse.ArgumentParser(description="Tests de algoritmos (corte, wave, coloreo, codigos, ciclicos, hungarian)")
    parser.add_argument("--impl", choices=list(MODULOS.keys()), help="Solo esta implementación")
    parser.add_argument("--list", action="store_true", help="Listar módulos y salir")
    args = parser.parse_args()

    if args.list:
        for name in MODULOS:
            print(name)
        return 0

    impls = list(MODULOS.keys()) if not args.impl else [args.impl]
    total_ok = 0
    total_fail = 0

    for impl in impls:
        mod_name = MODULOS[impl]
        print("\n--- %s ---" % impl)
        sys.path.insert(0, TESTS_DIR)
        try:
            mod = __import__(mod_name)
            ok, fail = mod.run()
            total_ok += ok
            total_fail += fail
        except Exception as e:
            print("  FAIL %s: no se pudo cargar/ejecutar: %s" % (impl, e))
            total_fail += 1
        finally:
            if TESTS_DIR in sys.path:
                sys.path.remove(TESTS_DIR)

    print("\nTotal: %d OK, %d FAIL" % (total_ok, total_fail))
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
