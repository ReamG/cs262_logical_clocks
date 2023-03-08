import consts
import time
from utils import print_progress_bar
from multiprocessing import Process
from machine import create_machine

def run_model():
    run = 223
    start_time = consts.get_time()

    pA = Process(target=create_machine, args=("A", run, start_time, 4))
    pB = Process(target=create_machine, args=("B", run, start_time, 5))
    pC = Process(target=create_machine, args=("C", run, start_time, 6))

    pA.start()
    pB.start()
    pC.start()

    GRANULARITY = 50
    progress = list(range(GRANULARITY))
    for i in progress:
        print_progress_bar(i, GRANULARITY, length=min(GRANULARITY,50))
        time.sleep(consts.EXPERIMENT_DURATION / GRANULARITY / 1000)

    pA.join()
    pB.join()
    pC.join()

if __name__ == "__main__":
    run_model()