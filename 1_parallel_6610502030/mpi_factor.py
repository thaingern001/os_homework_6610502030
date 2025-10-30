from mpi4py import MPI
from math import isqrt
import os ,sys ,resource

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
    if s > e:
        s, e = 1, 0
    return s, e

def mem_mb_peak():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r / (1024*1024) if sys.platform == "darwin" else r / 1024.0

def main():
    comm  = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    size  = comm.Get_size()

    if rank == 0:
        n = int(os.environ.get("N", "100000007"))
    else:
        n = None
    n = comm.bcast(n, root=0)

    limit = isqrt(n)
    s, e = split_ranges(limit, size, rank)

    comm.Barrier()
    t0 = MPI.Wtime()

    local = check_factorize(n, s, e) if s <= e else []

    # เก็บ peak memory ต่อโปรเซส
    mem_peak = mem_mb_peak()

    gathered = comm.gather(local,    root=0)
    mems     = comm.gather(mem_peak, root=0)

    t1 = MPI.Wtime()

    if rank == 0:
        factors = sorted(set(x for sub in gathered for x in sub))
        mem_max = max(mems)
        mem_avg = sum(mems)/len(mems)
        # พิมพ์เวลา + หน่วยความจำ เพื่อให้ benchmark.py regex จับได้
        print(f"n={n}  procs={size}  factors={len(factors)}  "
              f"time={t1 - t0:.6f}s  mem_max_mb={mem_max:.2f}  mem_avg_mb={mem_avg:.2f}")

if __name__ == "__main__":
    main()
