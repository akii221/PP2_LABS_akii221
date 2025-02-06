class PrimeFilter:
    def __init__(self, numbers):
        self.numbers = numbers
    
    def is_prime(self):
        return lambda x: x > 1 and all(x % i != 0 for i in range(2, int(x ** 0.5) + 1))

    def filter_primes(self):
        prime_lambda = self.is_prime()
        return list(filter(prime_lambda, self.numbers))


numbers = [2, 3, 4, 5, 6, 7]
prime_filter = PrimeFilter(numbers)

primes = prime_filter.filter_primes()

print(primes)
