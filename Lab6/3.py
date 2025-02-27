import os
def asd(path, path1):
    if os.access(path, os.F_OK) | os.access( path1, os.F_OK):
        print('Files: ')
        for entry in os.listdir(path1):
                if os.path.isfile(os.path.join(path1, entry)):
                 
                    print(entry)
        print('Dirs: ')
        for entry in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry)):
                   
                    print(entry)
    else:
         print('path doesnt exist')    

path = 'C:\\Users\\kat_0\\Desktop\\exampledirs'   
path1 = 'C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir'

asd(path, path1)
