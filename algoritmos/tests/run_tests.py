#!/usr/bin/env python3
"""
Ejecuta los tests de flujo máximo sobre todas las implementaciones que aceptan
entrada estándar en formato "x y c" (vértice origen, destino, capacidad).
Fuente = 0, sumidero = 1.

Uso (desde la raíz del repo o desde algoritmos/tests):
  python3 run_tests.py
  python3 run_tests.py --impl edmonds-karp
  python3 run_tests.py --list
"""
from __future__ import print_function

import os
import re
import subprocess
import sys
import argparse

# Directorio de este script
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
FLUJO_MAXIMO = os.path.join(TESTS_DIR, "flujo-maximo")

# Nombre visible de cada implementación
IMPL_DISPLAY_NAME = {"edmonds-karp-c": "Edmonds-Karp (C)"}

# Implementaciones: nombre -> (comando, cwd). Todo el código es Python 3.
def get_impls():
    impls = {}
    py = sys.executable
    # Python: edmonds-karp (verbosidad 0 para que solo imprima el valor al final)
    ek_dir = os.path.join(REPO_ROOT, "algoritmos", "edmonds-karp")
    if os.path.isdir(ek_dir):
        impls["edmonds-karp"] = ([py, "main.py", "-v", "0"], ek_dir)
    ek_letras_dir = os.path.join(REPO_ROOT, "algoritmos", "edmonds-karp-letras")
    if os.path.isdir(ek_letras_dir):
        impls["edmonds-karp-letras"] = ([py, "main.py", "-v", "0"], ek_letras_dir)
    # C: Edmonds-Karp (./main)
    ek_c_dir = os.path.join(REPO_ROOT, "algoritmos", "lab")
    main_c = os.path.join(ek_c_dir, "main")
    if os.path.isfile(main_c) and os.access(main_c, os.X_OK):
        impls["edmonds-karp-c"] = ([os.path.join(ek_c_dir, "main")], ek_c_dir)
    # Dinic: grafo fijo, sin entrada
    dinic_dir = os.path.join(REPO_ROOT, "algoritmos", "dinic")
    dinic_py = os.path.join(dinic_dir, "dinic.py")
    if os.path.isfile(dinic_py):
        impls["dinic"] = ([py, "dinic.py"], dinic_dir)
    return impls


def expected_from_filename(name):
    """Extrae el flujo esperado del nombre del archivo (debe_dar_N, simple_debe_dar_512, etc.)."""
    m = re.search(r"(?:^debe_dar_|_debe_dar_)(\d+)", name)
    if m:
        return int(m.group(1))
    return None


def extract_flow_value(output):
    """Extrae el valor del flujo maximal de la salida. Usa la última línea que indique flujo maximal (Edmonds-Karp en C imprime varias veces)."""
    last_flow = None
    for line in output.splitlines():
        if "flujo" in line.lower() and "maximal" in line.lower():
            nums = re.findall(r":\s*(\d+)", line)
            if nums:
                last_flow = int(nums[-1])
            else:
                nums = re.findall(r"\b(\d+)\s*$", line.strip())
                if nums:
                    last_flow = int(nums[-1])
    return last_flow


def run_one_test(impl_name, cmd_and_cwd, test_path):
    cmd, cwd = cmd_and_cwd
    if test_path is None:
        # Sin entrada (ej. dinic con grafo interno)
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
            )
            out, _ = proc.communicate(timeout=30)
            out = out.decode("utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            proc.kill()
            return None, "timeout"
        except Exception as e:
            return None, str(e)
        return extract_flow_value(out), None
    with open(test_path, "rb") as f:
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=f,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=cwd,
            )
            out, _ = proc.communicate(timeout=30)
            out = out.decode("utf-8", errors="replace")
        except subprocess.TimeoutExpired:
            proc.kill()
            return None, "timeout"
        except Exception as e:
            return None, str(e)
    return extract_flow_value(out), None


def main():
    parser = argparse.ArgumentParser(description="Tests de flujo máximo para todos los algoritmos")
    parser.add_argument("--impl", choices=["edmonds-karp", "edmonds-karp-letras", "edmonds-karp-c", "dinic"], help="Solo esta implementación")
    parser.add_argument("--list", action="store_true", help="Listar tests y salir")
    args = parser.parse_args()

    if not os.path.isdir(FLUJO_MAXIMO):
        print("No se encuentra el directorio de tests:", FLUJO_MAXIMO, file=sys.stderr)
        sys.exit(1)

    impls = get_impls()
    if args.impl:
        impls = {k: v for k, v in impls.items() if k == args.impl}
    if not impls:
        print("Ninguna implementación disponible (Edmonds-Karp en C requiere 'make' en algoritmos/lab).", file=sys.stderr)
        print("El resto usa Python 3.", file=sys.stderr)
        sys.exit(1)

    # Archivos de test con valor esperado en el nombre
    tests = []
    for f in sorted(os.listdir(FLUJO_MAXIMO)):
        path = os.path.join(FLUJO_MAXIMO, f)
        if not os.path.isfile(path):
            continue
        exp = expected_from_filename(f)
        if exp is not None:
            tests.append((f, path, exp))

    if args.list:
        for f, path, exp in tests:
            print("{} -> esperado {}".format(f, exp))
        return

    # Test especial para dinic (grafo interno, sin archivo de entrada)
    dinic_expected_path = os.path.join(TESTS_DIR, "dinic_expected.txt")
    dinic_expected = None
    if os.path.isfile(dinic_expected_path):
        try:
            with open(dinic_expected_path) as f:
                dinic_expected = int(f.read().strip())
        except (ValueError, IOError):
            pass

    total_ok = 0
    total_fail = 0
    for impl_name, cmd_cwd in impls.items():
        display = IMPL_DISPLAY_NAME.get(impl_name, impl_name)
        print("\n--- {} ---".format(display))
        if impl_name == "dinic":
            got, err = run_one_test(impl_name, cmd_cwd, None)
            if err:
                print("  FAIL (dinic grafo interno): {}".format(err))
                total_fail += 1
            elif got is None:
                print("  FAIL (dinic): no se pudo extraer el flujo")
                total_fail += 1
            elif dinic_expected is not None:
                if got == dinic_expected:
                    print("  OK   dinic grafo interno (flujo {})".format(got))
                    total_ok += 1
                else:
                    print("  FAIL dinic: esperado {}, obtuvo {}".format(dinic_expected, got))
                    total_fail += 1
            else:
                print("  OK   dinic grafo interno (flujo {}). Para validar: echo {} > dinic_expected.txt".format(got, got))
                total_ok += 1
            continue
        for name, path, expected in tests:
            got, err = run_one_test(impl_name, cmd_cwd, path)
            if err:
                print("  FAIL {}: {}".format(name, err))
                total_fail += 1
                continue
            if got is None:
                print("  FAIL {}: no se pudo extraer el flujo de la salida".format(name))
                total_fail += 1
                continue
            if got == expected:
                print("  OK   {} (flujo {})".format(name, got))
                total_ok += 1
            else:
                print("  FAIL {}: esperado {}, obtuvo {}".format(name, expected, got))
                total_fail += 1

    print("\nTotal: {} OK, {} FAIL".format(total_ok, total_fail))
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
