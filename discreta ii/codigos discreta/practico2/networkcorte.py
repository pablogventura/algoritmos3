n = {"s":[("a",4),("c",4)],
     "a":[("b",4),("d",2)],
     "c":[("b",2),("d",4)],
     "b":[("t",4)],
     "d":[("t",2)],
     "t":[]}

f = {("s","a"):4,
     ("s","c"):2,
     ("a","b"):4,
     ("a","d"):0,
     ("c","b"):0,
     ("c","d"):2,
     ("b","t"):4,
     ("d","t"):2}

def ntog(network):
    g = {}
    c = {}
    for v in network.keys():
        g[v] = []
        for (w,cap) in network[v]:
            g[v].append(w)
            c[(v,w)] = cap
        g[v].sort()
    return (g,c)

def corteminimal(network,f):
    """
    Devuelve un corte minimal usando bfs O(m).
    """
    (grafo,c) = ntog(network)
    q = [] # es una cola FIFO
    visitado = []
    q.append("s")
    visitado.append("s")
    result = []
    
    while q:
        v = q.pop(0) # lo toma del principio
        for w in sorted(grafo[v]):
            if w not in visitado and c[(v,w)] > f[(v,w)]:
                visitado.append(w)
                q.append(w) # lo inserta al final
                result.append((v,w))

    return visitado

def capacidadCorte(corte, network, f):
    result = 0
    (g,c) = ntog(network)
    for v in g:
        if v in corte:
            for w in g[v]:
                if w not in corte:
                    result += f[(v,w)]
        else:
            for w in g[v]:
                if w in corte:
                    result -= f[(v,w)]
    return result

def valorFlujo(f,network):
    result = 0
    (g,c) = ntog(network)
    for v in g:
        for w in g[v]:
            if w == "t":
                result += f[(v,w)]
    for w in g["t"]:
        result -= f[("t",w)]
    return result












