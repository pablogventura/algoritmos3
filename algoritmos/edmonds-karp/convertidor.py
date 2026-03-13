#!/usr/bin/env python
# encoding: utf-8

# este script adapta un archivo alfabetico a uno numerico.
# uso "python convertidor.py < entradaalfabetica > salidanumerica

import re

seguir = True


def reemplazar(v):
    if v == 's':
        return '0'
    elif v == 't':
        return '1'
    else:
        return str(ord(v))

while seguir:
    entrada = raw_input("")

    parseo = re.match("^(?P<x>[a-zA-Z])(?P<y>[a-zA-Z])(?P<cap>[0-9]+)$",
                      entrada)
    if parseo is not None:
        x = parseo.group("x")
        y = parseo.group("y")
        cap = int(parseo.group("cap"))

        print reemplazar(x) + " " + reemplazar(y) + " " + str(cap)

    else:
        seguir = False
