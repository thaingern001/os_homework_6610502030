from math import isqrt
import time
import os 
import sys, resource

def mem_mb_peak():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / (1024*1024) if sys.platform == "darwin" else r / 1024.0


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
    number = 10**15
    n = int(os.environ.get("N", str(number))) 
    t0 = time.perf_counter()
    factors = factorize(n)
    duration = time.perf_counter() - t0
    
    # print(f"n={n}  factors={len(factors)}  time={duration:.6f}s")
    print(f"n={n}  factors={len(factors)}  time={duration:.6f}s  mem_max_mb={mem_mb_peak():.2f}")
    
if __name__ == "__main__":
    main()