def sdf(N,B):
    for i in range(N,B+1):
        yield i * i

N = int(input('input first integer'))
B = int(input('input second integer'))

result = sdf(N,B)

for j in result:
    print(j)