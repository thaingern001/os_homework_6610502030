import subprocess as sp
import re
from pathlib import Path

RESULTS = Path("results")
RESULTS.mkdir(exist_ok=True)
CSV = RESULTS / "times.csv"

# NS = []
# for i in range(2,17):
#     NS.append(10**i + 3)
NS = [1_000_003, 10_000_019, 100_000_007]  # ตัวอย่าง n (แก้เพิ่มได้)
PROCS_LIST = [1, 2, 4, 8]                   # จำนวน process สำหรับ MPI

TIME_RE = re.compile(r"time\s*=\s*([0-9.]+)s")

def run_serial(n: int) -> float:
    env = {"N": str(n), **dict(**os_environ())}
    out = sp.run(["python3", "serial_factor.py"], env=env, capture_output=True, text=True, check=True).stdout
    m = TIME_RE.search(out)
    if not m:
        raise RuntimeError(f"Cannot parse time from serial output:\n{out}")
    return float(m.group(1))

def run_mpi(n: int, procs: int) -> float:
    env = {"N": str(n), **dict(**os_environ())}
    # ใช้ entrypoint ของ mpi4py ให้ชัวร์ว่าอยู่ใน env ที่ถูกต้อง
    out = sp.run(["mpiexec", "-n", str(procs), "python3", "-m", "mpi4py", "mpi_factor.py"],
                 env=env, capture_output=True, text=True, check=True).stdout
    # เวลาอยู่ที่ rank 0 เท่านั้น
    m = TIME_RE.search(out)
    if not m:
        raise RuntimeError(f"Cannot parse time from MPI output:\n{out}")
    return float(m.group(1))

def os_environ():
    # ป้องกันกรณีที่มี environment แปลก ๆ ในบางระบบ
    import os
    return os.environ

def append_csv(mode: str, n: int, procs: int, t: float):
    header_needed = not CSV.exists()
    with CSV.open("a", encoding="utf-8") as f:
        if header_needed:
            f.write("mode,n,procs,time_s\n")
        f.write(f"{mode},{n},{procs},{t:.6f}\n")

if __name__ == "__main__":
    print("== Benchmark serial vs MPI ==")
    # Serial
    for n in NS:
        t = run_serial(n)
        append_csv("serial", n, 1, t)
        print(f"serial  n={n:<10}  time={t:.6f}s")

    # MPI
    for n in NS:
        for p in PROCS_LIST:
            t = run_mpi(n, p)
            append_csv("mpi", n, p, t)
            print(f"mpi     n={n:<10}  procs={p:<2}  time={t:.6f}s")

    print(f"\nSaved -> {CSV.resolve()}")
