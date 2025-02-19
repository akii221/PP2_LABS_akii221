def trap(h,a,b):
    area = (a+b) * h / 2
    return area

h = int(input('Height'))
a = int(input('base first'))
b = int(input('base second'))

res = trap(h,a,b)
print(res)
