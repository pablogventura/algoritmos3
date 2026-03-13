#!/usr/bin/env python
# encoding: utf-8
from constants import *
from matrizcap import *
from bfslist import *
from caminoaumentante import *

import re

class EstadoEK(object):
    _cap = MatrizCap()
    flujoMaximal = 0
    _largoUltimoCamino = 0  # Para ir controlando el invariante

    def __init__(self, verbosidad=0):
        try:
            verbosidad = int(verbosidad)
        except ValueError:
            print "ERROR: La verbosidad debe ser un numero."
            print "Se asume verbosidad 0"
            verbosidad = 0

        if not verbosidad in verbosidades:
            print "ERROR: Valor de verbosidad no válido."
            print "Se asume verbosidad 0"
            verbosidad = 0
        self._cantCaminos = 0
        self._verbosidad = verbosidad

    def leer_un_lado(self):
        try:
            entrada = raw_input("")
        except EOFError:
            return 0

        parseo = re.match("^(?P<x>[0-9]+) (?P<y>[0-9]+) (?P<cap>[0-9]+)$",
                          entrada)
        #usa expresiones regulares para parsear la entrada
        #busca tres grupos de numeros enteros separados por espacios
        #cada uno esta etiquetado("?P<etiqueta>") con x, y, cap respectivamente
        if parseo is not None:
            x = int(parseo.group("x"))
            y = int(parseo.group("y"))
            cap = int(parseo.group("cap"))

            self._cap.agregarLado(x, y, cap)

            return 1

        else:
            return 0

    def aumentar_flujo(self):
    
        # Calcula el BFS
        self.bfs = BFS(self._cap)

        if self.bfs.llegoAlResumidero:
            
            # Armo el camino aumentante
            caminoAumentante = CaminoAumentante(self.bfs, self._cap)
            self._cantCaminos += 1

            # Controlo el invariante del largo de los caminos
            try:
                assert self._largoUltimoCamino <= len(caminoAumentante)
            except AssertionError:
                return -1

            self._largoUltimoCamino = len(caminoAumentante)

            if self._verbosidad in [1, 11, 101, 111]:

                print ("Incremento en el camino aumentante " +
                       str(self._cantCaminos) + ": " + str(caminoAumentante.flujo()))

            elif self._verbosidad in [2, 12, 102, 112]:
                print "-"*80
                print "BFS " + str(self._cantCaminos) + ":"
                print self.bfs
                
                print "camino aumentante " + str(self._cantCaminos) + ":"
                print caminoAumentante

            return 1 # porque se pudo aumentar
        else:

            self.flujoMaximal = self._cap.flujoDesdeFuente()

            # calculo la capacidad del corte minimal para asegurarnos
            corteMinimal = self.bfs.corteMinimal()
            capCorteMinimal = self._cap.capacidadCorte(corteMinimal)

            # controlo el invariante de la capacidad y el flujo
            try:
                assert capCorteMinimal == self.flujoMaximal
            except AssertionError:
                return -1

            if self._verbosidad in [0, 1, 2, 10, 11, 12]:
                print "No hay mas caminos aumentantes."
            elif self._verbosidad in [100, 101, 110, 111, 112]:
                print "No hay mas caminos aumentantes."
                strCorte = "S = {"
                for elem in self.bfs.corteMinimal():
                    if elem == fuente:
                        strCorte += "s, "
                    elif elem == resumidero:
                        strCorte += "t, "
                    else:
                        strCorte += chr(elem) + ", "
                strCorte = strCorte[:-2]  # Borro el ultimo ", "
                strCorte += "}"
                print "Corte Minimal: " + strCorte
                print "Capacidad: " + str(capCorteMinimal)
            return 0 # porque no se pudo aumentar

    def imprimir_flujo_maximal(self):

        if self._verbosidad in [10, 11, 12, 110, 111, 112]:
            print "Flujo Maximal:"
            print self._cap
            pass

        print "Valor del flujo maximal : " + str(self.flujoMaximal)

