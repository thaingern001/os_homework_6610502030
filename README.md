# 💻 Operating System Homework — Experiments Overview

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชา **Operating System (01204112)**  
ภาควิชาวิศวกรรมคอมพิวเตอร์ มหาวิทยาลัยเกษตรศาสตร์  
ประกอบด้วยการทดลอง **2 หัวข้อหลัก** เพื่อศึกษาการทำงานของระบบปฏิบัติการในมุมของ  
- **การประมวลผลแบบขนาน (Parallel Processing)**  
- **การจัดการหน่วยความจำ (Memory Management)**  

---

## 🧩 1. Parallel Factorization with MPI4Py

**โฟลเดอร์:** [`1_parallel_6610502030/`](./1_parallel_6610502030)

การทดลองนี้อยู่ภายใต้หัวข้อ **Introduction to Parallel Programming**  
โดยใช้ภาษา **Python (MPI4Py)** เพื่อคำนวณการหาตัวประกอบของจำนวนเต็ม (Factorization)  
ในรูปแบบของ **Parallel Computing** และเปรียบเทียบกับแบบ Sequential

**วัตถุประสงค์หลัก**
- ศึกษาการทำงานของ Message Passing Interface (MPI)
- เปรียบเทียบเวลาในการทำงาน (Execution Time) และการใช้หน่วยความจำ
- วิเคราะห์ Speedup, Efficiency และ Parallel Fraction ตาม Amdahl’s Law

**สรุปผลโดยย่อ**
- เมื่อเพิ่มจำนวนโพรเซส ความเร็วในการประมวลผลเพิ่มขึ้นอย่างชัดเจน
- Efficiency สูงสุดในช่วง 2–4 โพรเซส (~80–95%)
- สัดส่วนงานที่ขนานได้จริง (Parallel Fraction) ประมาณ **0.9**
- ใช้หน่วยความจำคงที่ต่อโพรเซส (~25 MB)

> 📈 โค้ดและผลการทดลองแบบละเอียดอยู่ในโฟลเดอร์  
> 👉 [`1_parallel_6610502030/`](./1_parallel_6610502030)

---

## 💾 2. Copy-On-Write (COW)

**โฟลเดอร์:** [`2_cow_6610502030/`](./2_cow_6610502030)

การทดลองนี้อยู่ภายใต้หัวข้อ **Memory Management in Operating System**  
โดยใช้ภาษา **C** เพื่อศึกษากลไก **Copy-On-Write (COW)** ซึ่งเป็นเทคนิคที่ระบบปฏิบัติการใช้  
ในการลดการคัดลอกหน่วยความจำระหว่างโปรเซสแม่และลูก (`fork()`)

**วัตถุประสงค์หลัก**
- สังเกตพฤติกรรมของหน่วยความจำเมื่อใช้ `fork()`
- วัดค่า Resident Set Size (VmRSS) ก่อนและหลังการเขียนข้อมูล
- แสดงให้เห็นว่าการคัดลอกหน่วยความจำจะเกิดขึ้นเฉพาะเมื่อมีการ “เขียนจริง”

**สรุปผลโดยย่อ**
- เมื่อไม่เขียนข้อมูลเลย (0%) → ไม่เกิดการคัดลอก หน่วยความจำแชร์ร่วมกันทั้งหมด  
- เมื่อเพิ่มสัดส่วนการเขียน (25%, 50%, 100%) → VmRSS ของโปรเซสลูกเพิ่มขึ้นตามสัดส่วน  
- กราฟผลลัพธ์มีลักษณะเชิงเส้น (Linear) ยืนยันแนวคิดของ Copy-On-Write

> 🧠 โค้ดและผลการทดลองแบบละเอียดอยู่ในโฟลเดอร์  
> 👉 [`2_cow_6610502030/`](./2_cow_6610502030)

---

## 🧮 Summary Comparison

| หัวข้อ | ภาษา / เครื่องมือ | แนวคิดหลัก | สิ่งที่ศึกษา | ผลลัพธ์สำคัญ |
|:-------|:------------------|:------------|:--------------|:---------------|
| **Parallel Programming** | Python + MPI4Py | Parallel Processing / Data Parallelism | Speedup, Efficiency, Memory usage | การขนานเพิ่มประสิทธิภาพ ~4.6x ที่ 8 โพรเซส |
| **Copy-On-Write (COW)** | C (GCC) | Memory Sharing & Copy-on-Write | การใช้หน่วยความจำ (VmRSS) | หน่วยความจำเพิ่มตามสัดส่วนการเขียนข้อมูล |

---

## ⚙️ Environment

- **OS:** Ubuntu Desktop 22.04 LTS  
- **Hardware:** Multi-core CPU, RAM ≥ 8 GB  
- **Python:** 3.10 + mpi4py  
- **Compiler:** gcc  
- **Visualization:** matplotlib, pandas  

---

## 📚 Reference

- Silberschatz, Galvin, Gagne — *Operating System Concepts (10th Edition)*  
- Peter S. Pacheco — *An Introduction to Parallel Programming*  
- Linux Manual Pages: `fork()`, `/proc/[pid]/status`, `waitpid()`, and memory management  
- MPI4Py Documentation — [https://mpi4py.readthedocs.io](https://mpi4py.readthedocs.io)

---

### ✍️ จัดทำโดย
**Thaingern Pinta**  
Computer Engineering, Kasetsart University  
📧 thaingern.p@ku.th  
