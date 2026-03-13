ndinic1 ={"0A":144,
    "0B":96,
    "0N":150,
    "AC":100,
    "AD":70,
    "AF":85,
    "AL":17,
    "BC":10,
    "BD":17,
    "BG":102,
    "BL":35,
    "C1":80,
    "CJ":5,
    "D1":80,
    "EC":100,
    "ED":15,
    "EG":10,
    "FH":15,
    "FK":100,
    "G1":80,
    "H1":20,
    "HM":40,
    "ID":22,
    "IG":10,
    "JA":5,
    "K1":120,
    "LH":30,
    "LK":60,
    "M1":30,
    "NE":110,
    "NI":40}

nejemplomaxi={"0A":8,
    "0C":7,
    "0D":10,
    "0E":7,
    "AF":4,
    "AG":3,
    "AI":8,
    "CG":2,
    "CH":3,
    "CJ":5,
    "DF":4,
    "DG":2,
    "EF":3,
    "EG":5,
    "EH":4,
    "F1":7,
    "G1":5,
    "H1":4,
    "I1":9,
    "J1":15}

n1={"0A":50,
    "0L":30,
    "0Y":70,
    "AB":120,
    "AQ":64,
    "BC":30,
    "BD":50,
    "BE":20,
    "CF":50,
    "CG":50,
    "DG":100,
    "EG":10,
    "EH":100,
    "FI":15,
    "GI":20,
    "GJ":100,
    "GK":20,
    "HK":5,
    "I1":45,
    "J1":20,
    "K1":100,
    "LM":30,
    "MN":30,
    "NP":30,
    "PG":30,
    "QR":50,
    "RU":40,
    "UV":33,
    "VW":67,
    "WX":123,
    "X1":232,
    "YB":30}
    

n2={"0F":20,
    "0I":20,
    "0P":60,
    "PA":60,
    "AB":20,
    "AC":20,
    "AD":15,
    "AE":20,
    "B1":5,
    "BG":5,
    "BH":5,
    "C1":5,
    "CG":5,
    "CH":5,
    "D1":5,
    "DG":10,
    "DH":5,
    "E1":5,
    "EG":5,
    "EH":5,
    "FB":5,
    "FC":5,
    "FD":5,
    "FE":5,
    "FI":10,
    "FJ":5,
    "G1":10,
    "GJ":15,
    "H1":10,
    "HJ":10,
    "IG":10,
    "IH":10,
    "IQ":20,
    "JQ":100,
    "QR":200,
    "R1":150}

n3={"0A":19,
    "0B":19,
    "0C":15,
    "AD":14,
    "AE":19,
    "AF":10,
    "BD":9,
    "BE":4,
    "BG":14,
    "CE":9,
    "CG":4,
    "D1":9,
    "E1":16,
    "FH":8,
    "G1":16,
    "H1":10}

n4={"0A":16,
    "0B":16,
    "0C":16,
    "AD":10,
    "AE":10,
    "AF":10,
    "AN":10,
    "BD":10,
    "BE":10,
    "BF":10,
    "CF":10,
    "CG":10,
    "DH":3,
    "DI":3,
    "DJ":3,
    "DK":3,
    "EH":3,
    "EI":3,
    "EJ":3,
    "EK":3,
    "FH":3,
    "FI":3,
    "FJ":3,
    "FK":3,
    "GH":3,
    "GI":3,
    "GJ":3,
    "GK":3,
    "HP":20,
    "IP":20,
    "JQ":20,
    "KQ":20,
    "NB":1,
    "NM":100,
    "MC":1,
    "MX":100,
    "PR":27,
    "QR":50,
    "R1":100,
    "XY":100,
    "YQ":100}


class Wave(object):
    def __init__(self,nw):
        self.s = "0"
        self.t = "1"
        self.vertices = set([x[0] for x in nw.keys()] + [x[1] for x in nw.keys()])
        self.nw = nw
        self.nwc=dict(nw)
        self.nwg=dict(nw)
        for k in self.nwg:
            self.nwg[k] = 0
        self.reset()
        self.ddddd=0
        
    def reset(self):
        self.B = {k : 0 for k in self.vertices} # No bloqueado
        self.D = {k : 0 for k in self.vertices} # desbalanceo cero

        self.N = set([self.s]) # conjunto de no balanceados
        
        self.naux = self.na(self.nwc,self.nwg)
        self.c=dict(self.naux)
        for k in self.c:
            self.c[k] = self.c[k][0]#me quedo solo con la capacidad
        self.g=dict(self.naux)
        for k in self.g:
            self.g[k] = 0
        self.gammaMas = dict()
        for v in self.vertices:
            self.gammaMas[v] = set(self.vecinosMas(v,self.naux))
        self.gammaMenos = dict()
        for v in self.vertices:
            self.gammaMenos[v] = set([])
    
    def io(self,f,nw):
        out_s = 0
        for x in self.vecinosMas(self.s,nw):
            out_s += f[self.s+x]
        in_t = 0
        for x in self.vecinosMenos(self.t,nw):
            in_t += f[x+self.t]
        return (out_s,in_t)
        
    def vecinosMas(self,v, n):
        result = []
        for lado in n:
            if lado[0] == v:
                result += lado[1]
        result.sort()
        return result

    def vecinosMenos(self,v, n):
        result = []
        for lado in n:
            if lado[1] == v:
                result += lado[0]
        result.sort()
        return result    

    def na(self,c,f):
        result = {}
        q = [] # es una cola FIFO
        visitado = {}
        q.append("0")
        visitado["0"] = 0
        #result = {}
        #for v in grafo:
        #    result[v] = []
        
        while q:
            v = q.pop(0) # lo toma del principio
            for w in self.vecinosMas(v,c):
                if "1" not in visitado or w == "1":
                    if (w not in visitado or visitado[w] == visitado[v] + 1) and c[v+w]-f[v+w] > 0:
                        visitado[w] = visitado[v] + 1
                        q.append(w) # lo inserta al final
                        result[v+w] = (c[v+w]-f[v+w],False)
            for w in self.vecinosMenos(v,c):
                if "1" not in visitado or w == "1":
                    if (w not in visitado or visitado[w] == visitado[v] + 1) and f[w+v] > 0:
                        visitado[w] = visitado[v] + 1
                        q.append(w) # lo inserta al final
                        result[v+w] = (f[w+v],True)

        return result



    def ordenBFS(self):
        """
        Devuelve el orden BFS de un grafo desde un origen dado.
        """
        global gammaMas
        q = [] # es una cola FIFO
        visitado = []
        q.append("0")
        visitado.append("0")
        
        while q:
            v = q.pop(0) # lo toma del principio
            for w in self.gammaMas[v]:
                if w not in visitado:
                    q.append(w) # lo inserta al final
                    if w == self.t:
                        return visitado[1:] # para sacar a s y no devolver t
                        
                    visitado.append(w)
        
        return visitado[1:] # para sacar a s
    def actualizar_flujo(self,g):
        for lado in self.naux.keys():
            flujo = self.g[lado]
            backward = self.naux[lado][1]
            
            if not backward:
                # es forward
                self.nwg[lado] += flujo
            else:
                # es backward
                self.nwg[lado[::-1]] -= flujo
                
    def wave(self):
        na = 1
        while self.t in set([x[0] for x in self.naux.keys()] + [x[1] for x in self.naux.keys()]):
            print("-" *80)
            print("Flujo bloqueante sobre network auxiliar %s" % na)
            fb = self.flujo_bloqueante()
            print("\ts = -%s\n\tt =  %s" % self.io(self.g,self.naux))
            self.actualizar_flujo(fb)
            self.reset()
            na+=1
        print("*" * 80)
        print("Flujo final:")
        print("\ts = -%s\n\tt =  %s" % self.io(self.nwg,self.nw))

        return self.nwg
        
    def flujo_bloqueante(self):
        try:
            for x in sorted(self.gammaMas[self.s]):
                self.g[self.s+x] = self.c[self.s+x] # mandamos todo lo que podemos sin importarnos el futuro
                self.D[x] = self.c[self.s+x] # x quedo desbalanceado
                self.N.add(x) # se agrega al conjunto de no balanceados
                self.gammaMenos[x] = set([self.s]) # mande flujo de s a x.

            obfs = self.ordenBFS()
            while self.N != set([self.s,self.t]):

                if obfs[0] == self.s:
                    obfs = obfs[1:]
                if obfs[-1] == self.t:
                    obfs = obfs[:-1]
                #FOR x ="s + 1" TO "t - 1" DO:  # BFS orden. (Begin INCREASEFLOW)
                for x in obfs:
                    if self.B[x] == 0 and self.D[x] > 0:
                        self.FORWARDBALANCE(x)
                     # solo balanceamos los desbalanceados que no esten bloqueados.
                # end INCREASEFLOW
                #FOR x ="t - 1" TO "s + 1" DO:  # reverse BFS orden. (Begin DECREASEFLOW)
                for x in reversed(obfs):
                    if self.B[x] == 1 and self.D[x] > 0:
                        self.BACKWARDBALANCE(x)
                     # solo balanceamos los desbalanceados que SI esten bloqueados.
                # end DECREASEFLOW
        except KeyboardInterrupt:
            pass
            
        return self.g


    def FORWARDBALANCE(self,x):
        while self.D[x] > 0 and self.gammaMas[x] != set([]):
            y = sorted(self.gammaMas[x])[0]
            if self.B[y] == 1:
                self.gammaMas[x].discard(y) # si esta bloqueado no podemos mandar flujo
            else:

                A = min(self.D[x], self.c[x+y] - self.g[x+y])
                self.g[x+y] = self.g[x+y] + A
                self.D[x] = self.D[x] - A
                self.D[y] = self.D[y] + A
                self.N.add(y) # como es un conjunto, si y ya estaba, no hace nada.
                self.gammaMenos[y].add(x)
                if self.g[x+y] == self.c[x+y]:
                    self.gammaMas[x].discard(y)


        if self.D[x] > 0:
            self.B[x] = 1 # si luego de todo quedo desbalanceado, se bloquea
        else:
            self.N.discard(x) # si D(x) = 0, debemos sacarlo de los no balanceados
        
        
        
        
    def BACKWARDBALANCE(self,x):
        while self.D[x] > 0 : # backward balance siempre tiene exito
            y = sorted(self.gammaMenos[x])[0]

            A = min(self.D[x], self.g[y+x]) # lo maximo que puedo devolver
            self.g[y+x] = self.g[y+x] - A
            self.D[x] = self.D[x] - A
            self.D[y] = self.D[y] + A
            self.N.add(y)
            if self.g[y+x] == 0:
                self.gammaMenos[x].discard(y)

        self.N.discard(x)
    
print("Ejercicio 1"    )
d=Wave(n1)
d.wave()
print("")
print("Ejercicio 2"    )
d=Wave(n2)
d.wave()
print("")
print("Ejercicio 3"    )
d=Wave(n3)
d.wave()
print("")
print("Ejercicio 4"    )
d=Wave(n4)
d.wave()
print("")
    
    
    
    
    
    
    
    
    
