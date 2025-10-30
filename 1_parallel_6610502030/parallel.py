# parallel.py
import subprocess as sp
import csv
from collections import defaultdict
from pathlib import Path
from datetime import datetime
import math
import os

RESULTS = Path("results")
CSV = RESULTS / "times.csv"
REPORT = RESULTS / "report.md"

def run_benchmark():
    print("▶ Running benchmark.py ...")
    sp.run(["python3", "benchmark.py"], check=True)

def run_visualize():
    print("▶ Running gen_visualize.py ...")
    sp.run(["python3", "gen_visualize.py"], check=True)

def load_rows():
    rows = []
    with CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "mode": r["mode"],
                "n": int(r["n"]),
                "procs": int(r["procs"]),
                "time": float(r["time_s"]),
                "mem_max_mb": float(r["mem_max_mb"]) if r.get("mem_max_mb") else None,
                "mem_avg_mb": float(r["mem_avg_mb"]) if r.get("mem_avg_mb") else None,
            })
    return rows

def summarize(rows):
    by_n = defaultdict(list)
    for r in rows:
        by_n[r["n"]].append(r)

    lines = []
    lines.append(f"# Parallel Factorization Summary\n")
    lines.append(f"- Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    lines.append(f"- Source: `{CSV}`\n")
    lines.append("")

    for n, items in sorted(by_n.items()):
        # หาเวลา serial อ้างอิง
        t1 = None
        for r in items:
            if r["mode"] == "serial" and r["procs"] == 1:
                t1 = r["time"]
                break
        if t1 is None:
            continue

        # ดึงชุด MPI
        mpi = sorted([r for r in items if r["mode"] == "mpi"], key=lambda x: x["procs"])
        if not mpi:
            continue

        lines.append(f"## n = {n}\n")
        lines.append("| procs | time(s) | speedup | efficiency | mem_max(MB) | mem_avg(MB) |")
        lines.append("|------:|--------:|--------:|-----------:|------------:|------------:|")

        best_S, best_p = None, None
        for r in mpi:
            p = r["procs"]
            S = t1 / r["time"] if r["time"] > 0 else float("nan")
            E = S / p
            mem_max = f"{r['mem_max_mb']:.2f}" if r["mem_max_mb"] is not None else ""
            mem_avg = f"{r['mem_avg_mb']:.2f}" if r["mem_avg_mb"] is not None else ""
            lines.append(f"| {p} | {r['time']:.6f} | {S:.3f} | {E:.3f} | {mem_max} | {mem_avg} |")
            if best_S is None or S > best_S:
                best_S, best_p = S, p

        # ประมาณค่า P ด้วย p ที่ใหญ่สุด
        if best_S is not None and best_p and best_p > 1:
            # P̂ = (1 - 1/S) / (1 - 1/p)
            Phat = (1.0 - 1.0 / best_S) / (1.0 - 1.0 / best_p)
            lines.append(f"\n**Estimated parallel fraction (Amdahl)**:  **P̂ ≈ {Phat:.3f}**  (using p={best_p}, S={best_S:.2f})\n")
            lines.append(f"_Interpretation_: ~{Phat*100:.1f}% of work scales with p, the rest is serial/overhead.\n")
        lines.append("---\n")

    return "\n".join(lines)

def main():
    RESULTS.mkdir(exist_ok=True)
    # 1) benchmark
    run_benchmark()
    # 2) plots
    run_visualize()
    # 3) summary & report
    rows = load_rows()
    report_md = summarize(rows)
    REPORT.write_text(report_md, encoding="utf-8")
    print(f"Done.\n- CSV  : {CSV.resolve()}\n- Report: {REPORT.resolve()}\n")

if __name__ == "__main__":
    main()
