import re

def mat(s):
    pattern = '^[A-Z]_[A-Z]$'
    return bool(re.findall(pattern,s))

asd = ["A_A", "ab", "abb", "ac", "b", "aabb"]
for s in asd:
    print(f'{s}: {mat(s)}')
