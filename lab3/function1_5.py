import itertools

def print_permutations():
    text  = input("enter a string: ")
    
    permutations = itertools.permutations(text)
    
    for perm in permutations:
        print(''.join(perm))

print_permutations()
