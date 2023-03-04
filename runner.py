from multiprocessing import Process
from machine import create_machine

def run_model():
    pA = Process(target=create_machine, args=("A",))
    pB = Process(target=create_machine, args=("B",))
    pC = Process(target=create_machine, args=("C",))

    pA.start()
    pB.start()
    pC.start()

    pA.join()
    pB.join()
    pC.join()

if __name__ == "__main__":
    run_model()