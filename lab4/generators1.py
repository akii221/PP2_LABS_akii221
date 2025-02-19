def squareg(N):
    for i in range(1, N+1):
        yield i * i

N=5
squarenum = squareg(N)

for j in squarenum:
    print(j)