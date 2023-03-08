import matplotlib.pyplot as plt
import numpy as np
import sys

"""
USAGE:
python3 graph_qlengths.py <run_num1,run_num2,run_num3,...>
where run_numX is a run number from our experiment.
EXAMPLE:
python3 graph_qlengths.py 1,2,3
"""

for run_num in sys.argv[1].split(','):
    """
    Simply loops over every run number passed in as an argument and
    graphs the queue length of each machine vs system time.
    NOTE: As laid out in spec, we only log queue lengths on receive events.
    So this is a graph of queue lengths when events were received.
    """

    plt.clf()
    for machine in ['A', 'B', 'C']:
        """
        Get the log from each machine, filter for the RECEIVED events,
        and graph the queue length at the time of the event vs the time of the event.
        """

        events = []
        f = open('../output/' + machine + str(run_num) + '.out', "r")

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
        f.close()

    plt.xlabel("time (ms)")
    plt.ylabel("Queue Length (count of messages on read)")
    plt.legend()
    plt.savefig('../output/Queue_Lengths_run' + str(run_num) + '.png')