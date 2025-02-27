def poly(s):
    if s == s[::-1]:
        print("Yes")
    else:
        print("No")

s = input('write a string to check is it polyndrome: ')
poly(s)