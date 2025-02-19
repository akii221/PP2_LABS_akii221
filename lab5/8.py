import re
def asd(s):
    asdf = '[A-Z]?[a-z]+'
    return re.findall(asdf,s)

print(asd("HelloWorld"))