import os 
def writel(path, data):
    f = open(path, "w")
    for item in data:
        f.write(item)
    return f

path = "C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir\\2.txt"

data = ["CS2 ", "DOTA 2", "LOL ", "NFS "]
writel(path,data)