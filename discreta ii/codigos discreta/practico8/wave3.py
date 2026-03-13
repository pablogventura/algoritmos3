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

def ordenBFS(n):
    """
    Devuelve el orden BFS de un grafo desde un origen dado.
    """
    q = [] # es una cola FIFO
    visitado = []
    q.append("0")
    visitado.append("0")
    
    while q:
        v = q.pop(0) # lo toma del principio
        for w in vecinosMas(v,n):
            if w not in visitado:
                visitado.append(w)
                q.append(w) # lo inserta al final

    return visitado
