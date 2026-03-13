#!/usr/bin/env python
# encoding: utf-8
from constants import *
from collections import namedtuple

# Named Tuple para representar cada elemento del BFS
BfsElem = namedtuple("BfsElem", "vertice, padre, flujo, esBackward")

def vtos(vertice):
    if vertice == fuente:
        return "s"
    elif vertice == resumidero:
        return "t"
    elif 0 <= vertice <= 0x10FFFF:
        return chr(vertice)
    else:
        return str(vertice)

class BFS(object):

    
    def __init__(self, matrizcap):
        """
        Genera el bfs a partir de la matriz de capacidades.
        """
        self.linea1 ="("
        self.linea2 =" "
        self.linea3 =" "
        self.bfs = {} # La clave es el vertice y el valor es un BfsElem
        self.llegoAlResumidero = False
        self._cap = matrizcap
        self._cacheCorteMinimal = [] # aca se va a guardar el corte minimal

        for vecino in self._cap.gammaMas(fuente):
            if self._cap.noEstaSaturado(fuente, vecino):
                self.bfs[vecino]=(BfsElem(vecino,
                                        fuente,
                                        self._cap.capacidadActual(fuente,
                                                                  vecino),
                                        False))
                self.linea1 += ",%s    " % vtos(vecino)
                self.linea2 += ",%s    " % vtos(fuente)
                self.linea3 += ",%04d " % self._cap.capacidadActual(fuente,
                                                                  vecino)
        iterador = list(self.bfs.keys())  # una lista para poder ir iterando
        iterador.sort()
        for key in iterador:
            elem = self.bfs[key]
            for vecino in self._cap.gammaMas(elem.vertice):
                if self._estaEnBfs(vecino) == False:
                    if self._cap.noEstaSaturado(elem.vertice, vecino):

                        flujo = min(self._cap.capacidadActual(elem.vertice,
                                                              vecino),
                                    self._flujoBfs(elem.vertice))

                        self.bfs[vecino]=(BfsElem(vecino,
                                                elem.vertice,
                                                flujo,
                                                False))
                        self.linea1 += ",%s    " % vtos(vecino)
                        self.linea2 += ",%s    " % vtos(elem.vertice)
                        self.linea3 += ",%04d " % flujo
                        iterador.append(vecino) # lo agrego para iterar
                        if vecino == resumidero:
                            self.llegoAlResumidero = True
                            return None

            for vecino in self._cap.gammaMenos(elem.vertice):

                if self._estaEnBfs(vecino) == False:
                    if self._cap.tieneFlujo(vecino, elem.vertice):

                        flujo = min(self._cap.flujoActual(vecino,
                                                          elem.vertice),
                                    self._flujoBfs(elem.vertice))

                        self.bfs[vecino]=(BfsElem(vecino,
                                                elem.vertice,
                                                flujo,
                                                True))
                        self.linea1 += ",%s    " % vtos(vecino)
                        self.linea2 += ",%s-   " % vtos(elem.vertice)
                        self.linea3 += ",%04d " % flujo
                        iterador.append(vecino) # lo agrego para iterar

        if not self.llegoAlResumidero:
            self._cacheCorteMinimal = [0] + iterador
        self.linea1 += ")"
        

            

    def _flujoBfs(self, x):
        """
        Devuelve el flujo del vertice x en el BFS.
        """
        if x == fuente:
            return float("inf")  # La fuente tiene un flujo infinito en el BFS

        return self.bfs[x].flujo


    def devolver(self, x):
        """
        Devuelve el BfsElem que representa a x en el BFS.
        """
        if x == fuente:
            return BfsElem(fuente, "nan", float("inf"), False)

        return self.bfs[x]


    def _estaEnBfs(self, x):
        """
        Devuelve un booleano que dice si el vertice x ya esta en el BFS.
        """
        if x == fuente:
            return True

        return x in self.bfs

    def resumideroEnBfs(self):
        """
        Devuelve el BfsElem que representa al resumidero, o si no llego
        None.
        """
        if not self.llegoAlResumidero:
            return None

        return self.bfs[resumidero]

    def corteMinimal(self):
        """
        PRE: No se pudo llegar al resumidero:
        Devuelve la lista de los vertices que quedaron sin poder llegar al 
        resumidero
        """
        assert not self.llegoAlResumidero

        return self._cacheCorteMinimal
    def __str__(self):
        result = "%s\n%s\n%s" % (self.linea1,self.linea2,self.linea3)
                
        return result
        
        
        
        
        
        
        
        
        
