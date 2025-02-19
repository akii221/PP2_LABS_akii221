import re
def snake(s):
    asd = s.split('_')
    return ''.join(word.capitalize() for word in asd )

print(snake('privet_kak_dela'))