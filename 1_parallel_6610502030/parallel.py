from factor.algo import factor_trial, factor_pollard_rho
from factor.utils import now_iso, get_rss_mb, reduce_stats, save_json

def parse_args():
    # --n, --algo, --chunk, --max-iters, --output, --seed, --note
    ...

def main():
    # init MPI (ถ้ามี), ชั้น thread: FUNNELED เป็นค่าเริ่มต้น
    # เลือกอัลกอริทึมจาก args
    # วัดเวลา: total, comm, compute
    # เก็บ env: MPI size, hostname, Python, mpi4py, OpenMPI/MPICH version
    # reduce สถิติทั้งหมดที่ root
    # เขียนผล JSON
    ...

if __name__ == "__main__":
    main()
