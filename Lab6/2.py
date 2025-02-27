import os
    
def testpath(path):
    if os.access(path, os.F_OK):
        print('path exists')
    else: 
        print('path doesnt exist')

    if os.access(path, os.R_OK):
        print('path is readable')
    else: 
        print('path isnt readable')
    
    if os.access(path, os.W_OK):
        print('path is writable')
    else: 
        print('path isnt writable')
    
    if os.access(path, os.X_OK):
        print('path is executable')
    else: 
        print('path is not executable')

path = "C:\\Users\\kat_0\\Desktop\\exampledirs\\exampledir"
testpath(path)
    