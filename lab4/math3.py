import math

def asd(n, s):
    area = (n * s**2) / (4 * math.tan(math.pi / n))
    return area

n = int(input("input number of sides"))
s = int(input("input the length of a side"))

area = asd(n, s)

print(f"area:  {area}")
