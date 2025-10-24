import csv
from collections import defaultdict
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

if __name__ == "__main__":
    rows = load_data()

    # รวมตาม configuration (mode, procs)
    grouped = defaultdict(list)
    for r in rows:
        key = f"{r['mode']}_p{r['procs']}"
        grouped[key].append((r["n"], r["time"]))

    # พล็อตกราฟ Time vs n (แต่ละเส้นคือ configuration)
    plt.figure()
    plt.title("Execution Time vs Problem Size (n)")
    plt.xlabel("Problem Size (n)")
    plt.ylabel("Time (s)")

    for label, data in grouped.items():
        data.sort(key=lambda x: x[0])
        ns, ts = zip(*data)
        plt.plot(ns, ts, marker="o", label=label)

    plt.legend(title="Mode / Processes", loc="best")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig("results/time_vs_n.png", dpi=160)
    plt.show()

    print("Saved -> results/time_vs_n.png")
