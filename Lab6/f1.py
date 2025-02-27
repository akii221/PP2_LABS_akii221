def mult(a):
    mult1 = 1
    for i in a:
        mult1 *= i
    return mult1

a = list(map(int, input("write a list of numbers: ").split()))
print(mult(a))