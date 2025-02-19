import math
   
def radik(D):
        radik1 = D * (math.pi) / 180
        return radik1

D = int(input('write a degree'))

res = radik(D)
print(res)