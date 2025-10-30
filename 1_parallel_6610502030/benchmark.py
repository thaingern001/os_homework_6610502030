import subprocess as sp
import re
from pathlib import Path
import os

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)
CSV = RESULTS / "times.csv"

# สร้างชุด n = 10^i + 3  
NS = [10**i + 3 for i in range(2, 17)]

# จำนวน process สำหรับ MPI 
PROCS_LIST = [1, 2, 4, 8]

# regex stdout (rank 0)
TIME_RE     = re.compile(r"time\s*=\s*([0-9.]+)s")
MEM_MAX_RE  = re.compile(r"mem_max_mb\s*=\s*([0-9.]+)")
MEM_AVG_RE  = re.compile(r"mem_avg_mb\s*=\s*([0-9.]+)")  

def parse_time_mem(out: str):
    """คืน (time_s, mem_max_mb, mem_avg_mb or None) จาก stdout ของโปรแกรม"""
    mt = TIME_RE.search(out)
    if not mt:
        raise RuntimeError(f"Cannot parse time from output:\n{out}")
    t = float(mt.group(1))

    mm = MEM_MAX_RE.search(out)
    mem_max = float(mm.group(1)) if mm else None

    ma = MEM_AVG_RE.search(out)
    mem_avg = float(ma.group(1)) if ma else None

    return t, mem_max, mem_avg

def run_serial(n: int):
    env = os.environ.copy()
    env["N"] = str(n)
    out = sp.run(["python3", "serial_factor.py"],
                 env=env, capture_output=True, text=True, check=True).stdout
    return parse_time_mem(out)

def run_mpi(n: int, procs: int):
    env = os.environ.copy()
    env["N"] = str(n)
    out = sp.run(
        ["mpiexec", "-n", str(procs), "python3", "-m", "mpi4py", "mpi_factor.py"],
        env=env, capture_output=True, text=True, check=True
    ).stdout
    return parse_time_mem(out)

def append_csv(mode: str, n: int, procs: int, t: float, mem_max, mem_avg):
    header_needed = not CSV.exists()
    with CSV.open("a", encoding="utf-8") as f:
        if header_needed:
            f.write("mode,n,procs,time_s,mem_max_mb,mem_avg_mb\n")
        
        mem_max_str = "" if mem_max is None else f"{mem_max:.6f}"
        mem_avg_str = "" if mem_avg is None else f"{mem_avg:.6f}"
        f.write(f"{mode},{n},{procs},{t:.6f},{mem_max_str},{mem_avg_str}\n")

if __name__ == "__main__":
    print("== Benchmark serial vs MPI ==")

    # Serial
    for n in NS:
        t, mem_max, mem_avg = run_serial(n)
        append_csv("serial", n, 1, t, mem_max, mem_avg)
        print(f"serial  n={n:<10}  time={t:.6f}s  mem_max={mem_max}MB")

    # MPI
    for n in NS:
        for p in PROCS_LIST:
            t, mem_max, mem_avg = run_mpi(n, p)
            append_csv("mpi", n, p, t, mem_max, mem_avg)
            print(f"mpi     n={n:<10}  procs={p:<2}  time={t:.6f}s  mem_max={mem_max}MB  mem_avg={mem_avg}MB")

    print(f"\nSaved -> {CSV.resolve()}")
