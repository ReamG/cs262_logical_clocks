import matplotlib.pyplot as plt
import numpy as np
import sys

"""
USAGE:
python3 clock_graphing.py <file1> <file2> <file3> ...
where fileX is a path to an output file from our experiment.
EXAMPLE:
python3 clock_graphing.py ../output/A1.out ../output/B1.out ../output/C1.out
"""

for file in sys.argv[1:]:
    """
    Simply loops over every file passed in as an argument and 
    graphs the clock time of each machine vs system time.
    """

    events = []

    # Extract clock time and system time from each line of the file
    f = open(file, "r")
    for line in f.readlines():
        delims = line.split(",")
        delims[-1] = delims[-1][:-1]
        events.append(delims)


    a_events = []
    a_rtimes = []
    a_ctimes = []

    # Create lists of real times, clock times, and events
    for e in events[1:]:
        a_events.append(e[0])
        a_rtimes.append(int(e[-2]))
        a_ctimes.append(int(e[-1]))

    # Compare to list that increases linearly at the rate of system time
    one2one = np.arange(len(a_rtimes)) + 1

    plt.clf()
    plt.plot(a_rtimes, a_ctimes, linestyle='dotted', label='Clock Times')
    plt.plot(a_rtimes, one2one, label="One to One Line")
    plt.title(f"Clock Time of Machine: {events[0][1]}, With Clock Rate: {events[0][2]} ticks/sec")
    plt.xlabel("(Real World) Time (ms)")
    plt.ylabel("Clock Time")
    plt.legend()
    plt.savefig(file.split('.out')[0] + '_clock_time_graph.png')

    f.close()
