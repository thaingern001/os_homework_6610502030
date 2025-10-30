import pandas as pd
from pathlib import Path

# ====== ตั้งค่า ======
RESULTS = Path("results")
FILES = [RESULTS / f"times{i}.csv" for i in range(1, 6)]  # times1–times5.csv
OUTFILE = RESULTS / "times_avg.csv"

# ====== โหลดไฟล์ทั้งหมด ======
dfs = [pd.read_csv(f) for f in FILES if f.exists()]
if not dfs:
    raise FileNotFoundError("ไม่พบไฟล์ times1.csv–times5.csv")

# ====== รวมทุกไฟล์เข้าด้วยกัน ======
df_all = pd.concat(dfs, ignore_index=True)

# ====== แปลงคอลัมน์เป็นตัวเลข (กัน error จาก string) ======
for col in ["time_s", "mem_max_mb", "mem_avg_mb"]:
    df_all[col] = pd.to_numeric(df_all[col], errors="coerce")

# ====== รวมเฉลี่ยตาม mode, n, procs ======
df_avg = (
    df_all.groupby(["mode", "n", "procs"], as_index=False)
    .agg({
        "time_s": "mean",
        "mem_max_mb": "mean",
        "mem_avg_mb": "mean"
    })
)

# ====== จัดรูปแบบทศนิยมให้เหมือนเดิม ======
df_avg["time_s"] = df_avg["time_s"].round(6)
df_avg["mem_max_mb"] = df_avg["mem_max_mb"].round(6)
df_avg["mem_avg_mb"] = df_avg["mem_avg_mb"].round(6)

# ====== เขียนไฟล์ผลลัพธ์ ======
df_avg.to_csv(OUTFILE, index=False, float_format="%.6f")

print(f"✅ Saved averaged results with same format -> {OUTFILE.resolve()}")
