

n1 ={"0A":144,
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

n2={"0A":15,
    "0D":20,
    "0J":7,
    "AB":17,
    "AH":5,
    "BC":15,
    "C1":20,
    "DC":26,
    "DE":5,
    "DG":10,
    "DI":6,
    "EF":5,
    "EK":2,
    "F1":5,
    "GK":10,
    "GM":3,
    "GO":1,
    "HN":4,
    "IF":4,
    "JL":7,
    "K1":10,
    "LB":5,
    "LN":4,
    "M1":1,
    "NC":6,
    "O1":10}

n3={"0A":20,
    "0B":69,
    "0C":145,
    "AD":14,
    "AE":19,
    "AF":18,
    "BD":9,
    "BE":4,
    "BF":14,
    "BH":1,
    "CE":190,
    "CF":4,
    "CH":20,
    "CI":20,
    "D1":9,
    "DH":8,
    "DI":1,
    "DJ":7,
    "E1":16,
    "EH":2,
    "EI":16,
    "EJ":7,
    "F1":146,
    "GI":5,
    "H1":25,
    "I1":15,
    "J1":7}

n4={"0U":160,
    "0V":50,
    "0W":100,
    "AH":20,
    "AN":10,
    "BH":10,
    "BI":20,
    "CI":10,
    "CJ":20,
    "DJ":15,
    "DK":20,
    "EK":15,
    "EL":20,
    "FL":15,
    "FM":20,
    "GM":15,
    "GN":10,
    "H1":20,
    "I1":20,
    "J1":20,
    "K1":20,
    "L1":20,
    "M1":20,
    "N1":20,
    "PA":20,
    "PB":20,
    "PC":20,
    "PD":20,
    "PE":20,
    "PF":20,
    "PG":25,
    "QX":50,
    "QZ":50,
    "RX":50,
    "RZ":50,
    "UX":60,
    "UY":200,
    "UZ":100,
    "VQ":70,
    "VR":20,
    "WQ":70,
    "WR":30,
    "X1":60,
    "YP":200,
    "Z1":100}
    
nw={"0A":8,
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

import networkx as nx
import matplotlib.pyplot as plt


def back(esBack):
    if esBack:
        return "-"
    else:
        return ""

def corrigenumero(tupla):
    (a,b)=tupla
    if tupla[0] == "0":
        a = "s"
    elif tupla[0] == "1":
        a = "t"
    elif tupla[0].isdigit():
        a = str(int(tupla[0])-1)
    if tupla[1] == "0":
        b = "s"
    elif tupla[1] == "1":
        b = "t"
    elif tupla[1].isdigit():
        b = str(int(tupla[1])-1)
    return (a,b)


def ppnetwork(G,archivo):
    pos=nx.graphviz_layout(G,prog='dot',args='')
    plt.figure(figsize=(8,8))

    nx.draw(G,pos,node_size=200,alpha=1,node_color="white", with_labels=True)
    plt.axis('equal')
    plt.savefig('%s.png' % archivo)
    plt.show()


def vecinosMas(v, n):
    result = []
    for lado in n:
        if lado[0] == v:
            result += lado[1]
    result.sort()
    return result

def vecinosMenos(v, n):
    result = []
    for lado in n:
        if lado[1] == v:
            result += lado[0]
    result.sort()
    return result



def na(c,f):
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
        for w in vecinosMas(v,c):
            if "1" not in visitado or w == "1":
                if (w not in visitado or visitado[w] == visitado[v] + 1) and c[v+w]-f[v+w] > 0:
                    visitado[w] = visitado[v] + 1
                    q.append(w) # lo inserta al final
                    result[v+w] = (c[v+w]-f[v+w],False)
        for w in vecinosMenos(v,c):
            if "1" not in visitado or w == "1":
                if (w not in visitado or visitado[w] == visitado[v] + 1) and f[w+v] > 0:
                    visitado[w] = visitado[v] + 1
                    q.append(w) # lo inserta al final
                    result[v+w] = (f[w+v],True)

    return result


def caminoDFS(na,f,c):
    """
    Devuelve el arbol DFS de un grafo desde un origen dado.
    """
    s = [] # es una pila LIFO
    visitado = []
    s.append("0")
    visitado.append("0")
    result={}
    #for v in grafo:
    #    result[v] = []
    
    while s:
        v = s[-1] # lo toma del final
        agrego = False
        for w in vecinosMas(v,na):
            #print((v,w))
            if w not in visitado:
                agrego = True 
                visitado.append(w)
                s.append(w) # lo inserta al final
                if not na[v+w][1]: # no es backward
                    result[v+w] = (c[v+w]-f[v+w],False)
                else: # es backward
                    result[v+w] = (f[w+v],True)
                if w == "1":
                    return result
                break
        if not agrego:
            for w in vecinosMas(v,result): # llegar a v no aporto nada
                del result[v+w] # no me hizo avanzar lo borro
            for w in vecinosMenos(v,result): # llegar a v no aporto nada
                del result[w+v] # no me hizo avanzar lo borro
            del s[-1] # lo borra porque todos sus vecinos fueron visitados
    
    return result

def ppcamino(c):
    result = ""
    try:
        fc = min([c[vw][0] for vw in c])
    except Exception:
        fc = 0
    
    v = "0"
    result += v
    w = vecinosMas(v,c)
    while w:
        try:
            assert (len(w) == 1)
        except Exception:
            #print(c)
            raise KeyError
        w = w[0]
        if not c[v+w][1]: # no es backward

            result += "," + w
        else: # es backward
            result += "<" + w
        v = w
        w = vecinosMas(w,c)
    result += ":%s" % fc
    return result

def actualizaNA(na,camino,f,c):
    fc = min([camino[vw][0] for vw in camino]) # el flujo del camino
    for (v,w) in camino:
        if not camino[v+w][1]: # no es backward
            f[v+w] += fc
            na[v+w] = (na[v+w][0]-fc,na[v+w][1]) # o sea na[v+w][0] -= fc
            print("\t\tLa cap de %s quedo en %s" % (v+w, c[v+w] - f[v+w]))
            if na[v+w][0] == 0:
                print("\t\t\tSe saturo %s en el NA" % (v+w))
                del na[v+w]
        else: # es backward
            f[w+v] -= fc
            na[v+w] = (na[v+w][0]-fc,na[v+w][1]) # o sea na[v+w][0] -= fc
            print("\t\tLa cap de %s quedo en %s" % (w+v, c[w+v] - f[w+v]))
            if na[v+w][0] == 0:
                print("\t\t\tSe saturo %s en el NA" % (v+w))
                del na[v+w]

def caminos(ne):
    result = set()
    n = dict(ne)
    f = dict(ne)
    for k in f:
        f[k] = 0
    cna = 0
    cca = 0
    aux = na(n,f)
    cna +=1
    print("")
    print("NA %s -----------" % cna)
    print(aux)
    ppnetwork(aux,str(cna))
    while "1" in [k[1] for k in aux]:
        c = caminoDFS(aux,f,n)
        for k in c:
            if k[0] != "0" and k[1] != "1":
                if c[k][1]:
                    kt = k[1]+str(ord(k[0])-65-15+1)
                    result.discard(kt)
                else:
                    kt = k[0]+str(ord(k[1])-65-15+1)
                    result.add(kt)
        cca += 1
        print("\tCam %s: %s" % (cca, ppcamino(c)))
        while "1" in [k[1] for k in c]:
            actualizaNA(aux,c,f,n)
            c = caminoDFS(aux,f,n)
            for k in c:
                if k[0] != "0" and k[1] != "1":
                    if c[k][1]:
                        kt = k[1]+str(ord(k[0])-65-15+1)
                        result.discard(kt)
                    else:
                        kt = k[0]+str(ord(k[1])-65-15+1)
                        result.add(kt)
            cca += 1
            print("\tCam %s: %s" % (cca, ppcamino(c)))
        aux = na(n,f)
        cna +=1
        print("")
        print("NA %s -----------" % cna)
        print(aux)
        ppnetwork(aux,str(cna))
    # para matchings return sorted(result)
    return f

print(caminos(nw))
