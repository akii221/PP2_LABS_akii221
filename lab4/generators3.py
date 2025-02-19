def foth(N):
    for i in range(0,N+1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


N = int(input("write a number"))
defg = foth(N)

for j in defg:
    print(j)