import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
USAGE:
python3 graph_stats.py <run_num1,run_num2,run_num3,...>
where run_numX is a run number from our experiment.
EXAMPLE:
python3 graph_stats.py 11,12,13,14,15,16
NOTE: This test assumed that the runs you pass into it are from
experiments where B and C were initialized with ticks=6, and A was
initialized with some value ticks=[1,2,3,4,5,6]. It studies the
relationship between the number of ticks in A's clock and the
number of logical jumps in the system, looking at average and
variance.
"""

meta_jumps = []

for run_num in sys.argv[1].split(','):
    f = open('../output/A' + str(run_num) + '.out', "r")
    lines = f.readlines()
    init_event = lines[0].split(',')
    machineName = init_event[1]
    tickRate = int(init_event[2])

    logicalJumps = []
    for lx in range(1,len(lines)-1):
        this_time = int(lines[lx].split(',')[-1])
        next_time = int(lines[lx+1].split(',')[-1])
        logicalJumps.append(next_time - this_time)
    
    meta_jumps.append(logicalJumps)
    
    f.close()

# Make a box and whisker plot of the logical jumps
plt.clf()
plt.boxplot(meta_jumps)
plt.title("Logical Jumps in System\n(Assuming B and C Initialized with Ticks=6)")
plt.xlabel("Number of Ticks in A's Clock")
plt.ylabel("Size of Logical Jumps")
plt.savefig('../output/Logical_Jumps_vs_Ticks.png')
