e1 = ["12553829",
"98898813",
"31589658",
"91793885",
"89248599",
"98388981",
"54891898",
"88918311"]

e2 = ["988566868",
"567423656",
"555223439",
"874555464",
"858653777",
"877455757",
["10","7","9","7","7","5","8","8","8"],
"777455757",
"857553777"]


e3 =[["31", "42", "7", "4", "11", "2", "7"],
["2", "5", "31", "3", "10", "768", "768"],
["6", "10", "31", "768", "11", "5", "1"],
["2", "2", "3", "9", "10", "4", "99"],
["4", "4", "2", "6", "3", "10", "7"],
["3", "10", "8", "4", "5", "99", "31"],
["31", "42", "10", "768", "6", "2", "3"]]

import dinic

def minmax(mentra):
    m=[]
    for fila in mentra:
        m.append([])
        for elem in fila:
            m[-1].append(str(elem))
    
    result = []
    v = set(reduce(lambda x,y: list(x) + list(y),m))
    v = map(int,list(v))
    v = sorted(v)
    print v
    while v:
        umbral = v[len(v)/2]
        print "el umbral es %s" % umbral
        nu = []
        for i in m:
            #print i
            temp = ""
            for j in i:
                if int(j) <= umbral:
                    temp += "1"
                else:
                    temp += "0"
            nu.append(temp)
        
        mat = dinic.caminos(mtog(nu))
        print "el matchin es perfecto = %s" % esperfecto(mat,nu)
        if esperfecto(mat,nu):
            #para un lado
            v = v[:len(v)/2]
            result = mat,umbral
        else:
            #para el otro
            v = v[len(v)/2+1:]
        print "ahora los valores posibles son %s" % v
        print "-"*80
    return result




def mtog(m):
    result = {}
    for letra in range(len(m)):
        result["%s%s"%("0",chr(65+letra))] = 1
        for numero in range(len(m[letra])):
            result["%s%s"%(chr(65+15+numero),"1")] = 1
            if m[letra][numero] == "1":
                result["%s%s"%(chr(65+letra),chr(65+15+numero))] = 1
    return result


def esperfecto(mat,m):
    letras = set([chr(65 + i) for i in range(len(m))])
    numeros = set([str(i + 1) for i in range(len(m[0]))])
    
    lm = set([k[0] for k in mat])
    nm = set([k[1] for k in mat])
    
    if letras == lm and numeros == nm:
        return True
    else:
        return False


#import dinic

#dinic.caminos(mtog(e1))
#raw_input()
#dinic.caminos(mtog(e2))
#raw_input()
#dinic.caminos(mtog(e3))
#raw_input()
#dinic.caminos(mtog(e4))
