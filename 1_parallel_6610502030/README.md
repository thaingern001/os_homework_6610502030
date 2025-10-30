

````markdown
# 🧮 Parallel Factorization with MPI4Py

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา **Intro to Parallel Programming**  
มีวัตถุประสงค์เพื่อศึกษาประสิทธิภาพของการประมวลผลแบบขนาน (Parallel Processing)  
โดยใช้ **MPI4Py** ในการหาตัวประกอบของจำนวนเต็มขนาดใหญ่ (Factorization)  
และเปรียบเทียบกับการคำนวณแบบลำดับ (Sequential)

---

## 📘 Overview

โครงการนี้ใช้หลักการของอัลกอริทึม **Trial Division Factorization**  
โดยแบ่งช่วงของตัวเลขจาก 1 ถึง √n ออกเป็นหลายส่วน  
แล้วให้แต่ละโพรเซสตรวจสอบช่วงของตนเองพร้อมกัน (Data Parallelism)  
เพื่อวัดประสิทธิภาพของระบบแบบขนานในด้านต่าง ๆ เช่น

- Execution Time  
- Speedup  
- Efficiency  
- Memory Usage  
- Parallel Fraction (Amdahl’s Law)

ผลการทดลองจะถูกรวบรวม วิเคราะห์ และสร้างกราฟอัตโนมัติ

---

## ⚙️ Project Structure

```bash
.
├── serial_factor.py      # การคำนวณแบบลำดับ (Sequential baseline)
├── mpi_factor.py         # การคำนวณแบบขนานด้วย MPI4Py
├── benchmark.py          # รันการทดลองหลายค่า n และ procs → บันทึกผล times.csv
├── gen_visualize.py      # สร้างกราฟเปรียบเทียบผลลัพธ์ (Time, Memory, Speedup)
├── parallel.py           # โปรแกรมหลัก (ควบคุม Benchmark + Graph + Summary)
├── results/
│   ├── times.csv         # ผลลัพธ์การทดลองดิบ
│   ├── times_avg.csv     # ผลเฉลี่ยหลายรอบ (option)
│   ├── *.png             # กราฟผลลัพธ์ที่สร้างโดย gen_visualize.py
│   └── report.md         # สรุปผลการทดลองอัตโนมัติ
└── README.md             # คู่มือโครงการ
````

---

## 🧩 Algorithm Principle

* ใช้อัลกอริทึม **Trial Division** ในการตรวจสอบตัวประกอบของจำนวนเต็ม n
* จำกัดช่วงตรวจสอบที่ ( 1 \leq i \leq \sqrt{n} )
* แบ่งช่วงตัวเลขออกเป็นหลายส่วนเท่า ๆ กันตามจำนวนโพรเซส (size)
* ใช้ **MPI4Py** จัดการโพรเซสแต่ละตัว และรวบรวมผลลัพธ์ด้วย `comm.gather()`
* การขนานนี้เป็นแบบ **Data Parallelism** ทำให้สามารถลดเวลาได้อย่างมีประสิทธิภาพ
  โดยเฉพาะเมื่อ n มีขนาดใหญ่มาก

---

## 🚀 How to Run

### 1. ติดตั้ง environment

```bash
pip install mpi4py matplotlib pandas
```

### 2. รันแบบ Sequential

```bash
python3 serial_factor.py
```

### 3. รันแบบ Parallel (MPI)

```bash
mpiexec -n 4 python3 -m mpi4py mpi_factor.py
```

### 4. รันการทดลองทั้งหมด (Benchmark + Graph + Report)

```bash
python3 parallel.py
```

ผลลัพธ์ทั้งหมดจะถูกเก็บไว้ในโฟลเดอร์ `results/` เช่น

* `times.csv` — ข้อมูลผลการทดลองทั้งหมด
* `*.png` — กราฟเปรียบเทียบเวลา, memory, speedup
* `report.md` — สรุปผลการทดลองพร้อมคำนวณ Speedup, Efficiency, และ Amdahl’s P

---

## 📈 Example Output

| Metric                | Trend                                      |
| --------------------- | ------------------------------------------ |
| **Speedup**           | สูงสุด ~4.6 เท่าที่ 8 โพรเซส               |
| **Efficiency**        | 80–95% (p ≤ 4), ลดลงเหลือ ~60% เมื่อ p = 8 |
| **Parallel Fraction** | เฉลี่ย ~0.9 (90% ของงานขนานได้จริง)        |
| **Memory Usage**      | คงที่ราว 25 MB ต่อโพรเซส                   |

> 💡 การคำนวณแบบขนานเริ่มมีประสิทธิภาพเมื่อขนาดของ n มีค่ามากกว่า (10^8)

---

## 🧠 Summary

* โปรแกรมสามารถทำงานแบบขนานได้จริงโดยใช้ **MPI4Py**
* ประสิทธิภาพเพิ่มขึ้นอย่างมีนัยสำคัญเมื่อขนาดของปัญหาใหญ่ขึ้น
* สอดคล้องกับทฤษฎีของ **Amdahl’s Law (P ≈ 0.9)**
* ใช้หน่วยความจำคงที่และเหมาะกับงานเชิงคำนวณ (CPU-bound)

---

## 📚 Reference

* *Silberschatz, Galvin, Gagne. Operating System Concepts, 10th Edition*
* *Peter S. Pacheco, An Introduction to Parallel Programming*
* *MPI4Py Documentation:* [https://mpi4py.readthedocs.io/](https://mpi4py.readthedocs.io/)

---

## 👨‍💻 Author

**Thaingern Pinta**
Department of Computer Engineering, Kasetsart University
📧 [thaingern.p@ku.th](mailto:thaingern.p@ku.th)

---