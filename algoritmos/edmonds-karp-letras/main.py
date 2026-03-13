#!/usr/bin/env python
# encoding: utf-8

from api import *

import optparse


def main():

    parser = optparse.OptionParser()
    parser.add_option("-v", "--verbose",
        help="Nivel de Verbosidad",
        default=0)
    options, args = parser.parse_args()

    ed = EstadoEK(options.verbose)

    result = 1
    while result == 1:
        result = ed.leer_un_lado()

    result = 1
    while result == 1:
        result = ed.aumentar_flujo()

    if result == -1:
        print "\nError al aumentar el flujo\n"
    else:
        ed.imprimir_flujo_maximal()

if __name__ == "__main__":
    main()
