#!/usr/bin/env python3
"""Tests para el módulo wave (red de flujo con aristas 'xy', fuente 0, sumidero 1)."""
import os
import sys
import importlib.util

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(TESTS_DIR, "..", ".."))
WAVE_DIR = os.path.join(REPO_ROOT, "algoritmos", "wave")
# Cargar wave por path para evitar conflicto con stdlib 'wave'
spec = importlib.util.spec_from_file_location("wave_mod", os.path.join(WAVE_DIR, "wave.py"))
wave_mod = importlib.util.module_from_spec(spec)
sys.modules["wave_mod"] = wave_mod
spec.loader.exec_module(wave_mod)


def test_vecinosMas():
    nw = wave_mod.nw
    out = wave_mod.vecinosMas("0", nw)
    assert "C" in out or "D" in out or "E" in out
    assert isinstance(out, list)


def test_vecinosMenos():
    nw = wave_mod.nw
    out = wave_mod.vecinosMenos("1", nw)
    assert "F" in out or "G" in out or "H" in out or "I" in out or "J" in out


def test_niveles():
    # Grafo mínimo 0 -> 1 para evitar bucles infinitos si la red es grande o hay desconexión
    red_chica = {"01": 10}
    niv = wave_mod.niveles(red_chica)
    assert len(niv) >= 2
    assert niv[0] == ["0"]
    assert "1" in (niv[1] if len(niv) > 1 else [])


def test_na():
    red_chica = {"01": 10}
    c = dict(red_chica)
    f = {k: 0 for k in c}
    res = wave_mod.na(c, f)
    assert isinstance(res, dict)
    assert "01" in res and res["01"][0] == 10


def test_wave_retorna_niveles():
    red_chica = {"01": 10}
    niv = wave_mod.wave(red_chica)
    assert isinstance(niv, list)
    assert len(niv) >= 1
    assert niv[0] == ["0"]


def run():
    ok = 0
    total = 5
    for name in ["test_vecinosMas", "test_vecinosMenos", "test_niveles", "test_na", "test_wave_retorna_niveles"]:
        try:
            globals()[name]()
            print("  OK   wave %s" % name)
            ok += 1
        except Exception as e:
            print("  FAIL wave %s: %s" % (name, e))
    return ok, total - ok
