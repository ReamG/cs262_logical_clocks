import matplotlib.pyplot as plt
import numpy as np
import sys

for run_num in sys.argv[1].split(','):

    plt.clf()
    for machine in ['A', 'B', 'C']:

        events = []
        f = open('output/' + machine + str(run_num) + '.out', "r")

        for line in f.readlines():
            delims = line.split(",")
            delims[-1] = delims[-1][:-1]
            events.append(delims)
        
        qlen = []
        readtimes = []

        for event in events:
            if event[0] == "RECEIVED":
                qlen.append(int(event[2]) + 1)
                readtimes.append(int(event[-2]))

        plt.scatter(readtimes, qlen, label='Machine ' + machine + f"(Clock Rate: {events[0][2]})")

    plt.xlabel("time (ms)")
    plt.ylabel("Queue Length (count of messages on read)")
    plt.legend()
    plt.savefig('output/Queue_Lengths_run' + str(run_num) + '.png')