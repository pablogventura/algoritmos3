def c(i,j,n):
    return (j-2*i)%n
    
    
for n in range(0,100):
    for i in range(n):
        for j in range(n):
            if i != n-1:
                if c(i,j,n) == c((i+1)%n,j,n):
                    print "derecha"
                    print (i,j,n)
            if j != n-1:
                if c(i,j,n) == c(i,(j+1)%n,n):
                    print "abajo"
                    print (i,j,n)
            if i != n-1 and j != n-1:
                if c(i,j,n) == c((i+1)%n,(j+1)%n,n):
                    print "diagonal"
                    print (i,j,n)

