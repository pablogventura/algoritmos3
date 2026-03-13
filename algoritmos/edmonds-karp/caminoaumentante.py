#!/usr/bin/env python
# encoding: utf-8
from constants import *
from collections import namedtuple

# Named Tuple para representar cada elemento del camino aumentante
CAElem = namedtuple("CAElem", "vertice, esBackward")

class CaminoAumentante:
    def __init__(self, bfs, matrizcap):
        """
        Calcula el camino aumentante a partir del bfs y la matriz de capacidades
        """
        self._camino=[] # lista que representa al camino aumentante
        self.bfs = bfs
        self._cap = matrizcap
        
        aux = self.bfs.resumideroEnBfs() # toma el resumidero

        self._flujo = aux.flujo # toma el flujo que es del camino aumentante

        self._camino.append(CAElem(aux.vertice, aux.esBackward)) # lo agrega
        while aux.vertice != fuente: # cuando llegue a la fuente termino
            if aux.esBackward:
                self._cap.flujoBackward(aux.padre, aux.vertice, self._flujo)
            else:
                self._cap.flujoForward(aux.padre, aux.vertice, self._flujo)

            aux = self.bfs.devolver(aux.padre) # va buscando al padre para seguir
            self._camino.append(CAElem(aux.vertice, aux.esBackward))

        self._camino.reverse() # quedo dado vuelta, lo arreglamos
        
    def __len__(self):
        """
        Devuelve el largo del camino para poder ver el invariante del largo de
        los caminos.
        """
        return len(self._camino)
        
    def flujo(self):
        """
        Devuelve el flujo del camino aumentante.
        """
        return self._flujo
        
    def __str__(self):
        """
        Devuelve un string con la impresion especificada.
        """
        strCamino = ""
        for (vertice, esBackward) in self._camino:
            if vertice == fuente:
                vertice = "s"
            elif vertice == resumidero:
                vertice = "t"
            else:
                vertice = chr(vertice) if 0 <= vertice <= 0x10FFFF else str(vertice)

            if esBackward:
                strCamino += "<" + str(vertice)
            else:
                strCamino += "," + str(vertice)

        strCamino = strCamino[1:]  # Borro la primer coma

        return strCamino + ": " + str(self.flujo())
