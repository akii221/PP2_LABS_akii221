import re
def mat(s):
    upper = 0
    pattern = '[A-Z]'
    upper = len(re.findall(pattern, s))
    return upper
def mat1(s):
    lower = 0
    pattern = '[a-z]'
    lower = len(re.findall(pattern, s))
    return lower


s = input("write a string")
print(mat(s), mat1(s))