

```markdown
# 🧠 Operating System Experiments
รายงานและการทดลองเกี่ยวกับ **การประมวลผลแบบขนาน (Parallel Programming)**  
และ **เทคนิค Copy-On-Write (COW)** ภายใต้หัวข้อรายวิชา *Operating System*  

---

## 📘 รายละเอียดโครงการ

โปรเจกต์นี้ประกอบด้วยการทดลอง 2 ส่วนหลัก ได้แก่

### 🧩 1. Introduction to Parallel Programming
การทดลองนี้ศึกษาการทำงานของ **โปรแกรมแบบขนาน (Parallel Programming)**  
โดยใช้ภาษา **Python (MPI4Py)** เพื่อคำนวณหาตัวประกอบของจำนวนเต็ม (Factorization)  
และเปรียบเทียบประสิทธิภาพระหว่าง  
- การทำงานแบบลำดับ (Sequential)  
- การทำงานแบบขนาน (Parallel)  

**วัตถุประสงค์**
- เข้าใจการสื่อสารระหว่าง process ด้วย MPI  
- เปรียบเทียบเวลาในการทำงานและการใช้หน่วยความจำ  
- วิเคราะห์ speedup และ efficiency ตามกฎของ Amdahl’s Law  

**ไฟล์ที่เกี่ยวข้อง**
```

parallel.py          # main program (MPI)
benchmark.py         # run multiple tests and collect data
gen_visualize.py     # plot and analyze results
factor/algo.py       # factorization algorithms
factor/utils.py      # helper functions (timer, RSS, JSON export)
results/             # experiment data and plots

````

**การรันโปรแกรม**
```bash
# ตัวอย่างการรันแบบขนาน
mpirun -np 4 python3 parallel.py --n 13082761331670030 --algo trial
````

---

### 💾 2. Copy-On-Write (COW)

การทดลองนี้ศึกษากลไกการจัดการหน่วยความจำของระบบปฏิบัติการ
โดยเฉพาะเทคนิค **Copy-On-Write (COW)** ซึ่งช่วยให้ process แม่และลูกแชร์หน่วยความจำร่วมกัน
และคัดลอกเฉพาะส่วนที่ถูกแก้ไขจริง (on write)

**วัตถุประสงค์**

* สังเกตพฤติกรรมของหน่วยความจำเมื่อใช้ `fork()`
* วัดปริมาณหน่วยความจำจริง (VmRSS) ก่อนและหลังการเขียน
* แสดงให้เห็นประสิทธิภาพของ COW ในการลดการคัดลอกหน่วยความจำ

**ไฟล์ที่เกี่ยวข้อง**

```
cow.c        # main source code
Makefile     # build and clean commands
```

**วิธีการคอมไพล์และรัน**

```bash
make                # คอมไพล์โปรแกรม
./cow 50 0.0        # ทดลอง 50MB เขียน 0%
./cow 50 0.25       # ทดลอง 50MB เขียน 25%
./cow 50 0.5        # ทดลอง 50MB เขียน 50%
./cow 50 1.0        # ทดลอง 50MB เขียน 100%
./cow 100 0.5       # ทดลอง 100MB เขียน 50%
```

**ผลลัพธ์ที่ได้ (ตัวอย่าง)**

```
[child] init VmRSS(kB)=640
[child] after write 50% VmRSS(kB)=26368
[parent] before wait VmRSS(kB)=1536
[parent] after wait VmRSS(kB)=1536
```

> ผลแสดงให้เห็นว่า VmRSS ของโปรเซสลูกเพิ่มขึ้นตามสัดส่วนของการเขียน
> ยืนยันการทำงานของ Copy-On-Write ว่าคัดลอกหน่วยความจำเฉพาะเมื่อมีการเขียนจริงเท่านั้น

---

## 📊 ผลการทดลองโดยสรุป

| ขนาดหน่วยความจำ | Write (%) | VmRSS หลังเขียน (kB) | สรุปผล                     |
| :-------------: | :-------: | :------------------: | :------------------------- |
|      50 MB      |     0%    |          896         | แชร์ทั้งหมด (ไม่คัดลอก)    |
|      50 MB      |    25%    |        13,568        | คัดลอกบางส่วน              |
|      50 MB      |    50%    |        26,368        | คัดลอกครึ่งหนึ่ง           |
|      50 MB      |    100%   |        51,968        | คัดลอกทั้งหมด              |
|      100 MB     |    50%    |        51,968        | หน่วยความจำเพิ่มตามสัดส่วน |

---

## ⚙️ สิ่งแวดล้อมที่ใช้ในการทดลอง

* OS: **Ubuntu Desktop 22.04 LTS**
* Compiler: **gcc (C experiment)**
* Python: **Python 3.10 + mpi4py**
* Hardware: Multi-core CPU, RAM ≥ 8 GB

---

## 📚 อ้างอิง

* Silberschatz, Galvin, and Gagne. *Operating System Concepts, 10th Edition.*
* Linux man page: `fork()`, `/proc/[pid]/status`, and memory management.
* MPI4Py Documentation: [https://mpi4py.readthedocs.io](https://mpi4py.readthedocs.io)

---

### ✍️ จัดทำโดย

**Thaingern Pinta**
Computer Engineering, Kasetsart University
MIKE LAB — Large Knowledge and Information Engineering Laboratory

```

