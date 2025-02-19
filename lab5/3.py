import re

def matchinsgs(s):
    pattern = '^[a-z]+_[a-z]$'
    return bool(re.findall(pattern,s))

asd = ["a_a", "ab", "abb", "ac", "b", "aabb"]

for s in asd:
    print(f'{s}: {matchinsgs(s)}')