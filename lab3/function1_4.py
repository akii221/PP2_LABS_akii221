def is_prime(n):
    if n <= 1:
        return False
    
    for i in range(2,int(n ** 0.5) + 1):
        if n & 1 == 0:
            return False
        
    return True
def filterprime(number):
    return list(filter(is_prime, number))

number = [1, 2, 3, 4, 5, 6, 7, 8, 0]
prime = filterprime(number)
print(prime)
