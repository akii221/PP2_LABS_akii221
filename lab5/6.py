import re
def kaka(s):
    pattern = '[ ,.]'
    return re.sub(pattern, ':', s)


text = "vsem privet, menya zovut danil."
print({kaka(text)})