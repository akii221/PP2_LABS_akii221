def dfg(N):
    for i in range(N, -1, -1):
       
            yield i

N = int(input('input integer'))

res = dfg(N)

for j in res:
    print(j)
