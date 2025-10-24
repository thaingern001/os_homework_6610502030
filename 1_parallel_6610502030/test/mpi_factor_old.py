# mpi_factor.py
from mpi4py import MPI
from math import isqrt
from time import time

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
    # แบ่งช่วง 1..limit เป็น parts ส่วน แล้วคืนช่วงของ rank=idx
    size = (limit + parts - 1) // parts
    s = idx * size + 1
    e = min((idx + 1) * size, limit)
    if s <= e :
        return (s, e)
    else :
        (1,0)

def main():
    
    comm  = MPI.COMM_WORLD
    rank  = comm.Get_rank()
    size  = comm.Get_size()

    # --- กำหนด n ที่ rank 0 แล้วกระจายให้ทุกคน ---
    if rank == 0:
        import os
        print("MPI Factorization Program1")
        start_time = time()
        number = 10**17
        n = int(os.environ.get("N", str(number)))  # เปลี่ยนได้ตอนรัน
    else:
        n = None
    n = comm.bcast(n, root=0)

    # --- แต่ละ process คิดช่วงของตัวเอง ---
    limit = isqrt(n)
    s, e  = split_ranges(limit, size, rank)

    # --- คำนวณของใครของมัน แล้วส่งกลับไปรวมที่ rank 0 ---
    local = check_factorize(n, s, e) if s <= e else []
    gathered = comm.gather(local, root=0)

    if rank == 0:
        # รวมผล (serial part)
        
        factors = sorted(set(x for sub in gathered for x in sub))
        end_time = time()
        print(f"n = {n}")
        print(f"procs = {size}")
        print(f"factors (first 20) = {factors[:20]}{' ...' if len(factors)>20 else ''}")
        print(f"total factors = {len(factors)}")
        print(f"computed in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
