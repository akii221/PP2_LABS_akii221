import re

def matchings(s):
    pattern = '^ab*$'
    return bool(re.findall(pattern,s))


asd = ["a", "ab", "abb", "ac", "b", "aabb"]
for s in asd:
    print(f"'{s}': {matchings(s)}")