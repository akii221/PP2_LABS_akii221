import re 
def kaka(s):
    return re.sub('_', "",s)

print(kaka("hey_you"))