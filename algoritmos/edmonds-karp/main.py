#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Punto de entrada del algoritmo Edmonds-Karp."""

import argparse
import sys

from api import EstadoEK


def main():
    parser = argparse.ArgumentParser(description="Edmonds-Karp: flujo máximo en red.")
    parser.add_argument(
        "-v", "--verbose",
        type=int,
        default=111,
        help="Nivel de verbosidad (default: 111)",
    )
    args = parser.parse_args()

    ek = EstadoEK(verbosidad=args.verbose)
    flujo = ek.run(stream=sys.stdin)

    if flujo == -1:
        print("\nError al aumentar el flujo\n", file=sys.stderr)


if __name__ == "__main__":
    main()
