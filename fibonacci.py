def fibonacci(n):
    """Generate Fibonacci sequence up to n terms"""
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

def fibonacci_generator(limit):
    """Generate Fibonacci numbers up to a value limit"""
    a, b = 0, 1
    while a <= limit:
        yield a
        a, b = b, a + b

if __name__ == "__main__":
    # First 20 terms
    print("First 20 Fibonacci numbers:")
    print(fibonacci(20))
    
    # Fibonacci numbers up to 1000
    print("\nFibonacci numbers up to 1000:")
    print(list(fibonacci_generator(1000)))
