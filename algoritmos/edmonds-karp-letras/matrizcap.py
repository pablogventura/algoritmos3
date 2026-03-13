#!/usr/bin/env python
# encoding: utf-8
from constants import *


class MatrizCap(object):
    matriz = {}
    gMas = {}
    gMenos = {}
    _cacheFlujoDesdeFuente = 0

    def agregarLado(self, x, y, cap):
        """
        Agrega un lado a la matriz de capacidades.
        Toma como argumentos los vertices (x,y) del lado y su capacidad.
        Inicializa el flujo actual en 0.
        """
        self.matriz[(x, y)] = (cap, 0)

        if x in self.gMas:
            self.gMas[x].append(y)
            self.gMas[x].sort()
        else:
            self.gMas[x] = [y]

        if y in self.gMenos:
            self.gMenos[y].append(x)
            self.gMenos[y].sort()
        else:
            self.gMenos[y] = [x]

    def capacidadTotal(self, x, y):
        """
        Devuelve la capacidad total del lado (x,y).
        """
        return self.matriz[(x, y)][0]

    def flujoActual(self, x, y):
        """
        Devuelve el flujo actual del lado (x,y).
        """
        return self.matriz[(x, y)][1]

    def capacidadActual(self, x, y):
        """
        Calcula y devuelve la capacidad actual del lado (x,y).
        """
        return self.capacidadTotal(x, y) - self.flujoActual(x, y)

    def gammaMas(self, x):
        """
        Toma un vertice x y devuelve una lista con todos sus vecinos +.
        """
        try:
            return self.gMas[x]
        except KeyError:
            return []

    def gammaMenos(self, x):
        """
        Toma un vertice x y devuelve una lista con todos sus vecinos -.
        """
        try:
            return self.gMenos[x]
        except KeyError:
            return []

    def noEstaSaturado(self, x, y):
        """
        Devuelve un booleano que indica si el lado (x,y) no esta saturado.
        """
        return self.capacidadTotal(x, y) > self.flujoActual(x, y)

    def tieneFlujo(self, x, y):
        """
        Devuelve un booleano que indica si el lado (x,y) tiene flujo.
        """
        return self.flujoActual(x, y) > 0

    def flujoDesdeFuente(self):
        """
        Devuelve el valor de todo el flujo que sale de la fuente.
        Cuando ya no hay mas caminos aumentantes es el flujo maximal.
        """

        return self._cacheFlujoDesdeFuente

    def flujoForward(self, x, y, flujo):
        """
        Modifica el valor del flujo actual en la matriz de capacidades.
        Toma el lado (x,y) y el flujo, y modifica la matriz teniendo en cuenta
        que es un flujo forward.
        """
        self.matriz[(x, y)] = (self.matriz[(x, y)][0],
                               self.matriz[(x, y)][1] + flujo)
        if x == fuente:
            self._cacheFlujoDesdeFuente += flujo

    def flujoBackward(self, x, y, flujo):
        """
        Modifica el valor del flujo actual en la matriz de capacidades.
        Toma el lado (x,y) y el flujo, y modifica la matriz teniendo en cuenta
        que es un flujo backward.
        """
        self.matriz[(y, x)] = (self.matriz[(y, x)][0],
                               self.matriz[(y, x)][1] - flujo)
                               
        if x == fuente:
            self._cacheFlujoDesdeFuente -= flujo
            
    def capacidadCorte(self, corte):
        """
        Toma una lista que representa un corte, y devuelve su capacidad.
        """
        capCorte = 0
        for elem in corte:
            for hijo in self.gammaMas(elem):
                if not hijo in corte:
                    if self.capacidadActual(elem, hijo) == 0:
                        capCorte += self.capacidadTotal(elem, hijo)
        return capCorte

    def __str__(self):
        """
        Devuelve un string usado para la representacion en pantalla de la
        matriz de capacidades.
        """
        cadena = ""
        claves = list(self.matriz.keys())
        claves.sort()
        for (x, y) in claves:
            flujo = str(self.matriz[(x, y)][1])
            if x == fuente:
                x = "s"
            elif x == resumidero:
                x = "t"
            else:
                x = chr(x).upper()
            if y == fuente:
                y = "s"
            elif y == resumidero:
                y = "t"
            else:
                y = chr(y).upper()

            cadena += "Lado " + str(x) + "," + str(y) + ": "
            cadena += flujo + "\n"

        return cadena[:-1]
