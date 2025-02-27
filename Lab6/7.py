import os 
def copys(path, path1):
    f = open(path, "r")
    content = f.read()
    d = open(path1, "w")
    d.write(content)
    f.close

path = "C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir\\1.txt"
path1 = "C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir\\3.txt"
copys(path,path1)

    