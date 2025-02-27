import os
def countl(path):
    f = open(path, "r")
    lines = f.readlines()
    return print(len(lines))

path = "C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir\\1.txt"
countl(path)