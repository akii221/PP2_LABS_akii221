import os

def listdirs(path):
        print('Dirs: ')
        for entry in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry)):
                   
                    print(entry)    
                    


def listdfils(path1):
        print('Files: ')
        for entry in os.listdir(path1):
                if os.path.isfile(os.path.join(path1, entry)):
                 
                    print(entry)  

def botf(path, path1):
        print("Dirs and Files:")
        for entry1 in os.listdir(path):
                if os.path.isdir(os.path.join(path, entry1)):
                   
                    print(entry1) 
        for entry in os.listdir(path1):
                if os.path.isfile(os.path.join(path1, entry)):
                 
                    print(entry)  
                   





path = 'C:\\Users\\kat_0\\Desktop\\exampledirs'   
path1 = 'C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir'  
listdirs(path)
listdfils(path1)
botf(path, path1)

        
        

