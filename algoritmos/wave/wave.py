from functools import reduce

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


def arbolBFS(grafo):
    """
    Devuelve el arbol BFS de un grafo desde un origen dado.
    """
    q = [] # es una cola FIFO
    visitado = []
    q.append("0")
    visitado.append("0")
    result = {}
    for v in grafo:
        result[v] = []
    
    while q:
        v = q.pop(0) # lo toma del principio
        for w in vecinosMas(v,grafo):
            if w not in visitado:
                visitado.append(w)
                q.append(w) # lo inserta al final
                result[v] += [w]
                result[w] += [v]
        result[v].sort()

    return result

def soloprim(lista):
    result = []
    for x in lista:
        if x not in result:
            result.append(x)
    return result

def niveles(n):
    result = [["0"]]
    temp = []
    while set([x[0] for x in n.keys()] + [x[1] for x in n.keys()]) != set(reduce(lambda x,y:x+y,result)):
        #print((set([x[0] for x in n.keys()] + [x[1] for x in n.keys()]), set(reduce(lambda x,y:x+y,result))))
        temp = []
        for x in result[-1]:
            temp += vecinosMas(x,n)
        #print((temp,soloprim(temp)))
        temp = soloprim(temp)            
        result.append(temp)
    return result

def wave(n):
    c=dict(n)
    f=dict(n)
    for k in f:
        f[k] = 0
    b={k:False for k in list(set([x[0] for x in n.keys()] + [x[1] for x in n.keys()]))}#bloqueados
    emu={k:[] for k in list(set([x[0] for x in n.keys()] + [x[1] for x in n.keys()]))}#bloqueados
    aux = na(c,f)
    niv = niveles(aux)
    l = reduce(lambda x,y:x+y,niv)
    v = l[0]
    for w in vecinosMas(v,aux);
        if not b(w):
            f[v+w]+=c[v+w]-f[v+w]
            emu[w].append(emu[-1]+c[v+w]-f[v+w])
    
    
    d["0"] = sum([c("0"+x) for x in vecinosMas(x,n
    return niv
    
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
