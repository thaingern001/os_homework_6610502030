from mpi4py import MPI

comm = MPI.COMM_WORLD   # communicator หลัก
rank = comm.Get_rank()  # หมายเลข process
size = comm.Get_size()  # จำนวน process ทั้งหมด

print(f"Hello from process {rank} of {size}")
