import matplotlib.pyplot as plt

# ข้อมูลจากการทดลอง
write_percent = [0, 25, 50, 100]
vmrss_50 = [896, 13568, 26368, 51968]
vmrss_100 = [896, 26368, 51968, 103168]

plt.figure(figsize=(8,5))
plt.plot(write_percent, vmrss_50, 'o-', label='50 MB', linewidth=2)
plt.plot(write_percent, vmrss_100, 's--', label='100 MB', linewidth=2)

plt.title("Results of the Copy-On-Write experiment (COW)\nWrite proportion (%) vs memory usage (VmRSS)")
plt.xlabel("writing proportion (%)")
plt.ylabel("VmRSS after writing (kB)")
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()
