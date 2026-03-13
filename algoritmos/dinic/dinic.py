

c ={"0A":144,
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

f ={"0A":0,
    "0B":0,
    "0N":0,
    "AC":0,
    "AD":0,
    "AF":0,
    "AL":0,
    "BC":0,
    "BD":0,
    "BG":0,
    "BL":0,
    "C1":0,
    "CJ":0,
    "D1":0,
    "EC":0,
    "ED":0,
    "EG":0,
    "FH":0,
    "FK":0,
    "G1":0,
    "H1":0,
    "HM":0,
    "ID":0,
    "IG":0,
    "JA":0,
    "K1":0,
    "LH":0,
    "LK":0,
    "M1":0,
    "NE":0,
    "NI":0}


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



def caminoDFS(na):
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
            #print (v,w)
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
    fc = min([c[vw][0] for vw in c])
    
    v = "0"
    result += v
    w = vecinosMas(v,c)
    while w:
        try:
            assert (len(w) == 1)
        except Exception:
            print(c)
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

def actualizaNA(na,camino,f):
    fc = min([camino[vw][0] for vw in camino]) # el flujo del camino
    for (v,w) in camino:
        if not camino[v+w][1]: # no es backward
            f[v+w] += fc
            na[v+w] = (na[v+w][0]-fc,na[v+w][1]) # o sea na[v+w][0] -= fc
            if na[v+w][0] == 0:
                del na[v+w]
        else: # es backward
            f[w+v] -= fc
            na[v+w] = (na[v+w][0]-fc,na[v+w][1]) # o sea na[v+w][0] -= fc
            if na[v+w][0] == 0:
                del na[v+w]

def caminos(n,f):
    result = []
    aux = na(n,f)
    while "1" in [k[1] for k in aux]:
        c = caminoDFS(aux)
        while "1" in [k[1] for k in c]:
            result.append(c)
            actualizaNA(aux,c,f)
            c = caminoDFS(aux)
        aux = na(n,f)
    result = list(map(ppcamino, result))
    for i in result:
        print(i)
    total = sum(f[k] for k in f if k[0] == "0")
    print("Valor del flujo maximal :", total)


if __name__ == "__main__":
    caminos(c, f)
