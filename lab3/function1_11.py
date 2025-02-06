def polyndrome(sent):
    sent1 = ''
    sent1 = sent[::-1]

    if sent1 == sent:
        return True
    return False

s = "malayalam"
print(polyndrome(s))

