#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Punto de entrada Edmonds-Karp (versión letras)."""

import argparse
import sys

from api import EstadoEK


def main():
    parser = argparse.ArgumentParser(description="Edmonds-Karp: flujo máximo (entrada con letras).")
    parser.add_argument("-v", "--verbose", type=int, default=0, help="Nivel de verbosidad")
    args = parser.parse_args()

    ek = EstadoEK(verbosidad=args.verbose)
    flujo = ek.run(stream=sys.stdin)

    if flujo == -1:
        print("\nError al aumentar el flujo\n", file=sys.stderr)


if __name__ == "__main__":
    main()
