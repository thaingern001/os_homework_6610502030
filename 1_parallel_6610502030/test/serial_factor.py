# serial_factor.py
from math import isqrt
import time

def factorize(n):
    factors = []
    for i in range(1, isqrt(n) + 1):
        if n % i == 0:
            factors.append(i)
            j = n // i
            if j != i:
                factors.append(j)
    return sorted(factors)

def main():
    n = 10**17  # ตัวอย่างเลขใหญ่
    start_time = time.time()
    factors = factorize(n)
    end_time = time.time()
    
    print(f"Factors of {n} (first 20): {factors[:20]}{' ...' if len(factors)>20 else ''}")
    print(f"Total factors found: {len(factors)}")
    print(f"Computed in {end_time - start_time:.4f} seconds")
    
    
if __name__ == "__main__":
    main()