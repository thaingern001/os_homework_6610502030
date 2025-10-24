import csv
from collections import defaultdict
import math
import matplotlib.pyplot as plt

CSV = "results/times.csv"

def load_data():
    rows = []
    with open(CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "mode": r["mode"],
                "n": int(r["n"]),
                "procs": int(r["procs"]),
                "time": float(r["time_s"]),
            })
    return rows

def group_by_n(rows):
    g = defaultdict(list)
    for r in rows:
        g[r["n"]].append(r)
    for n in g:
        g[n].sort(key=lambda x: (x["mode"], x["procs"]))
    return g

if __name__ == "__main__":
    rows = load_data()
    byn = group_by_n(rows)

    for n, items in byn.items():
        # หาเวลา serial อ้างอิง
        t1 = next((r["time"] for r in items if r["mode"] == "serial" and r["procs"] == 1), None)
        if t1 is None:
            continue

        procs = sorted({r["procs"] for r in items if r["mode"] == "mpi"})
        times = [next(r["time"] for r in items if r["mode"] == "mpi" and r["procs"] == p) for p in procs]
        speedup = [t1 / t for t in times]

        # Time vs Procs
        plt.figure()
        plt.title(f"Execution Time vs Processes (n={n})")
        plt.xlabel("Processes")
        plt.ylabel("Time (s)")
        plt.plot(procs, times, marker="o")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"results/time_n{n}.png", dpi=160)

        # Speedup vs Procs
        plt.figure()
        plt.title(f"Speedup vs Processes (n={n})")
        plt.xlabel("Processes")
        plt.ylabel("Speedup (T1 / Tp)")
        plt.plot(procs, speedup, marker="o")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"results/speedup_n{n}.png", dpi=160)

    print("Saved plots into results/: time_* and speedup_*")
