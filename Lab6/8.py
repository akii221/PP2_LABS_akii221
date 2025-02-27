import os 
def testpath(path):
    if os.access(path, os.F_OK):
        os.remove(path)
    else: 
        print('path doesnt exist')

path = "C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir\\deleteme.txt"
testpath(path)
