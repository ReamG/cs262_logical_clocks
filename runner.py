import consts
from multiprocessing import Process
from machine import create_machine

def run_model():
    run = 1
    start_time = consts.get_time()

    pA = Process(target=create_machine, args=("A", run, start_time))
    pB = Process(target=create_machine, args=("B", run, start_time))
    pC = Process(target=create_machine, args=("C", run, start_time))

    pA.start()
    pB.start()
    pC.start()

    pA.join()
    pB.join()
    pC.join()

if __name__ == "__main__":
    run_model()