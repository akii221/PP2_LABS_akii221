def evennum(N):
    for i in range(0, N+1):
        if i % 2 == 0:
            yield i
        

N = int(input('type a number'))
newg = evennum(N)

for j in newg:
    print(j)
        