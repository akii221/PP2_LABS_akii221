import re

def asdb(s):
    pattern = '^a.*b$'
    return bool(re.match(pattern,s))

asd = ["A_A", "ab", "abb", "ac", "b", "aabb"]
for s in asd:
    print(f'{s}: {asdb(s)}')
