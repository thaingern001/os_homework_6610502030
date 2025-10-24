from mpi4py import MPI
print("OK:", MPI.Get_library_version().splitlines()[0])