import time
import math

def roots(number, ms1):
    delay = ms1 / 1000
    time.sleep(delay)
    result = math.sqrt(number)
    return result


number = int(input("Write a number: "))
ms1 = int(input("Write milliseconds: "))

result = roots(number, ms1)
print(f'Square root of {number} after {ms1} milliseconds is {result}')