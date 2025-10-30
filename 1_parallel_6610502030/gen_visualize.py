import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime

CSV = "results/times.csv"

def load_data():
    rows = []
    with open(CSV, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            def f2float(s):
                s = (s or "").strip()
                return float(s) if s not in ("", None) else None
            rows.append({
                "mode":  r["mode"],
                "n":     int(r["n"]),
                "procs": int(r["procs"]),
                "time":  float(r["time_s"]),
                # ↓ รองรับคอลัมน์เมม (อาจว่างใน serial เก่าหรือไฟล์เก่า)
                "mem_max_mb": f2float(r.get("mem_max_mb", "")),
                "mem_avg_mb": f2float(r.get("mem_avg_mb", "")),
            })
    return rows

if __name__ == "__main__":
    rows = load_data()

    # ===== Time vs n (เดิม) =====
    grouped_time = defaultdict(list)
    for r in rows:
        key = f"{r['mode']}_p{r['procs']}"
        grouped_time[key].append((r["n"], r["time"]))

    plt.figure()
    plt.title("Execution Time vs Problem Size (n)")
    plt.xlabel("Problem Size (n)")
    plt.ylabel("Time (s)")
    plt.xscale("log", base=10)

    for label, data in grouped_time.items():
        data.sort(key=lambda x: x[0])
        ns, ts = zip(*data)
        plt.plot(ns, ts, marker="o", label=label)

    plt.legend(title="Mode / Processes", loc="best")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    fig_path = f"results/figs/time/time_vs_n_log_{now}.png"
    plt.savefig(fig_path, dpi=160)
    plt.show()
    print(f"Saved -> {fig_path}")

    # ===== Memory vs n (MAX) =====
    grouped_mem_max = defaultdict(list)
    for r in rows:
        if r["mem_max_mb"] is not None:
            key = f"{r['mode']}_p{r['procs']}"
            grouped_mem_max[key].append((r["n"], r["mem_max_mb"]))

    if grouped_mem_max:
        plt.figure()
        plt.title("Peak Memory (RSS max) vs Problem Size (n)")
        plt.xlabel("Problem Size (n)")
        plt.ylabel("Peak Memory (MB)")
        plt.xscale("log", base=10)

        for label, data in grouped_mem_max.items():
            data.sort(key=lambda x: x[0])
            ns, ms = zip(*data)
            plt.plot(ns, ms, marker="o", label=label)

        plt.legend(title="Mode / Processes", loc="best")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        fig_path = f"results/figs/mem_peak/mem_max_vs_n_log_{now}.png"
        plt.savefig(fig_path, dpi=160)
        plt.show()
        print(f"Saved -> {fig_path}")

    # ===== Memory vs n (AVG) – ถ้ามี =====
    grouped_mem_avg = defaultdict(list)
    for r in rows:
        if r["mem_avg_mb"] is not None:
            key = f"{r['mode']}_p{r['procs']}"
            grouped_mem_avg[key].append((r["n"], r["mem_avg_mb"]))

    if grouped_mem_avg:
        plt.figure()
        plt.title("Average Memory (RSS avg across ranks) vs Problem Size (n)")
        plt.xlabel("Problem Size (n)")
        plt.ylabel("Average Memory (MB)")
        plt.xscale("log", base=10)

        for label, data in grouped_mem_avg.items():
            data.sort(key=lambda x: x[0])
            ns, ms = zip(*data)
            plt.plot(ns, ms, marker="o", label=label)

        plt.legend(title="Mode / Processes", loc="best")
        plt.grid(True, linestyle="--", alpha=0.3)
        plt.tight_layout()
        fig_path = f"results/figs/mem_avg/mem_avg_vs_n_log_{now}.png"
        plt.savefig(fig_path, dpi=160)
        plt.show()
        print(f"Saved -> {fig_path}")
