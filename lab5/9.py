import re
def asd(s):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2',s)


print(asd('HelloMaBro'))        