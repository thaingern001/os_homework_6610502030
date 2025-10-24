# mpi_factor.py
from mpi4py import MPI
from math import isqrt
import time

def check_factorize(n, s, e):
    facs = []
    for i in range(s, e + 1):
        if n % i == 0:
            facs.append(i)
            j = n // i
            if j != i:
                facs.append(j)
    return facs

def split_ranges(limit, parts, idx):
    size = (limit + parts - 1) // parts
    s = idx * size + 1
    e = min((idx + 1) * size, limit)
    return (s, e)

def main():
    comm  = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    size  = comm.Get_size()

    if rank == 0:
        n = 100000007
    else:
        n = None
    n = comm.bcast(n, root=0)

    limit = isqrt(n)
    s, e = split_ranges(limit, size, rank)
    comm.Barrier()
    t0 = MPI.Wtime()

    local = check_factorize(n, s, e)
    gathered = comm.gather(local, root=0)

    t1 = MPI.Wtime()
    if rank == 0:
        factors = sorted(set(x for sub in gathered for x in sub))
        print(f"n={n}  procs={size}  factors={len(factors)}  time={t1-t0:.4f}s")

if __name__ == "__main__":
    main()
