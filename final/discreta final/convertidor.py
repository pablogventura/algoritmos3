#!/usr/bin/env python
# encoding: utf-8

# este script adapta un archivo alfabetico a uno numerico.
# uso "python convertidor.py < entradaalfabetica > salidanumerica

import re, sys

seguir = True

while seguir:
    try:
        entrada = raw_input("")
    except EOFError:
        sys.exit(0)
    while len(entrada):

        parseo = re.match("^[\s]*(?P<x>[a-zA-Z])[\s]*(?P<y>[a-zA-Z])[\s]*:[\s]*(?P<cap>[0-9]+)", entrada)
        if parseo is not None:
            x = parseo.group("x")
            y = parseo.group("y")
            cap = int(parseo.group("cap"))

            print str(x) + str(y) + " " + str(cap)
            entrada = entrada[parseo.end('cap'):]
        else:
            entrada = ""
