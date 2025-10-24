def check_factorize(target, start, end):
    factors = set()
    for i in range(start, end+1):
        if target%i == 0:
            factors.add(i)
            factors.add(target//i)
    factors = sorted(factors)
    return factors

def sequence_factorize(n):
    start = 1
    end = int(n**(1/2))
    factors = check_factorize(target = n, start = start, end= end)
    return factors

def parallel_factorize(n):
    start = 1
    end = int(n**(1/2))
    factors = check_factorize(target = n, start = start, end= end)
    return factors



def main():
    num = 10**20
    start = 1
    end = 10
    print(f"Factors of {num} from requence : {sequence_factorize(num)}")
    
    # print(f"Factors of {num} from {start} to {end}: {check_factorize(num, start, end)}")
    
    
if __name__ == "__main__":
    main()