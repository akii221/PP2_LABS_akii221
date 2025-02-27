import os 
def newf(path):
        filess = []
        for char in range(65, 91):
            files = os.path.join(path, chr(char)+'.txt')
            with open(files, "w"):
                filess.append(files)
        return filess

path = "C:\\Users\\kat_0\\Desktop\\exampledirs\\storage"
newf(path)