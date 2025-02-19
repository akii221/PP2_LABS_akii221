import re

def matchings(s):
    pattern = '^ab{2,3}$'
    return bool(re.findall(pattern,s))


text = ["a", "ab", "abb", "ac", "b", "aabb"]

for s in text:
    print(f"'{s}': {matchings(s)}")