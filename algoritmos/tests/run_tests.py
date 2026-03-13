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
import time

# Directorio de este script
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
FLUJO_MAXIMO = os.path.join(TESTS_DIR, "flujo-maximo")

# Nombre visible de cada implementación
IMPL_DISPLAY_NAME = {"edmonds-karp-c": "Edmonds-Karp (C)"}

# Nombres cortos para la tabla de tiempos
IMPL_SHORT_NAME = {
    "edmonds-karp": "EK Python",
    "edmonds-karp-letras": "EK letras",
    "edmonds-karp-c": "EK (C)",
}

# Implementaciones que comparten los mismos tests (flujo máximo) para comparar tiempos
IMPL_EDMONDS_KARP_FAMILY = frozenset({"edmonds-karp", "edmonds-karp-letras", "edmonds-karp-c"})

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


def _imprimir_comparativa_tiempos(tiempos_ek, tests):
    """Imprime tabla de tiempos entre las implementaciones Edmonds-Karp."""
    if not tiempos_ek or not tests:
        return
    test_names = [t[0] for t in tests]
    impls_orden = sorted(tiempos_ek.keys())
    w_name = min(28, max(10, max(len(n) for n in test_names) + 2))
    w_col = 11
    sep = "  "
    print("\n--- Comparativa de tiempos (Edmonds-Karp) ---")
    header_cells = ["Test".ljust(w_name)] + [
        IMPL_SHORT_NAME.get(i, IMPL_DISPLAY_NAME.get(i, i))[:w_col].ljust(w_col)
        for i in impls_orden
    ]
    print("  " + sep.join(header_cells))
    print("  " + "-" * (w_name + len(impls_orden) * (w_col + len(sep))))
    totales = {impl: 0.0 for impl in impls_orden}
    for name in test_names:
        cells = [name[: w_name - 1].ljust(w_name)]
        for impl in impls_orden:
            t = tiempos_ek[impl].get(name)
            if t is not None:
                totales[impl] += t
                cells.append(("%.3f s" % t).rjust(w_col))
            else:
                cells.append("-".rjust(w_col))
        print("  " + sep.join(cells))
    print("  " + "-" * (w_name + len(impls_orden) * (w_col + len(sep))))
    row_total = ["TOTAL".ljust(w_name)] + [
        ("%.3f s" % totales[impl]).rjust(w_col) for impl in impls_orden
    ]
    print("  " + sep.join(row_total))
    if totales and totales[min(totales, key=totales.get)] > 0:
        mas_rapido = min(totales, key=totales.get)
        mas_lento = max(totales, key=totales.get)
        ratio = totales[mas_lento] / totales[mas_rapido]
        print("  (más rápido: %s, ~%.2fx respecto al más lento)" % (
            IMPL_SHORT_NAME.get(mas_rapido, IMPL_DISPLAY_NAME.get(mas_rapido, mas_rapido)), ratio))


def run_one_test(impl_name, cmd_and_cwd, test_path):
    """Ejecuta un test. Devuelve (valor_flujo_o_None, error_o_None, tiempo_segundos)."""
    cmd, cwd = cmd_and_cwd
    t0 = time.perf_counter()
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
            return None, "timeout", time.perf_counter() - t0
        except Exception as e:
            return None, str(e), time.perf_counter() - t0
        return extract_flow_value(out), None, time.perf_counter() - t0
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
            return None, "timeout", time.perf_counter() - t0
        except Exception as e:
            return None, str(e), time.perf_counter() - t0
    return extract_flow_value(out), None, time.perf_counter() - t0


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
    # Tiempos por implementación y test (solo para las 3 Edmonds-Karp)
    tiempos_ek = {}  # impl_name -> { test_name -> segundos }

    for impl_name, cmd_cwd in impls.items():
        display = IMPL_DISPLAY_NAME.get(impl_name, impl_name)
        print("\n--- {} ---".format(display))
        if impl_name == "dinic":
            got, err, _ = run_one_test(impl_name, cmd_cwd, None)
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
            # Tests con grafos n2, n3, n4 (n1 ya cubierto arriba)
            try:
                grafos_script = os.path.join(TESTS_DIR, "test_dinic_grafos.py")
                proc = subprocess.Popen(
                    [sys.executable, grafos_script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=REPO_ROOT,
                )
                out_grafos, _ = proc.communicate(timeout=60)
                out_grafos = out_grafos.decode("utf-8", errors="replace")
                for line in out_grafos.strip().splitlines():
                    s = line.strip()
                    if s.startswith("OK") and "dinic" in s:
                        total_ok += 1
                        print("  " + s)
                    elif "FAIL" in s and "dinic" in s:
                        total_fail += 1
                        print("  " + s)
            except subprocess.TimeoutExpired:
                proc.kill()
                total_fail += 1
                print("  FAIL test_dinic_grafos: timeout")
            except Exception as e:
                total_fail += 1
                print("  FAIL test_dinic_grafos: {}".format(e))
            continue
        if impl_name in IMPL_EDMONDS_KARP_FAMILY:
            tiempos_ek[impl_name] = {}
        for name, path, expected in tests:
            got, err, elapsed = run_one_test(impl_name, cmd_cwd, path)
            if impl_name in IMPL_EDMONDS_KARP_FAMILY:
                tiempos_ek[impl_name][name] = elapsed
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

    # Comparativa de tiempos entre las implementaciones Edmonds-Karp
    if len(tiempos_ek) >= 2:
        _imprimir_comparativa_tiempos(tiempos_ek, tests)
    sys.exit(1 if total_fail else 0)


if __name__ == "__main__":
    main()
