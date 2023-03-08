# Analysis

## Ticks vs Average Logical Jump Size

Another thing we were interested in studying was the average jump in the logical clock value for machines initialized with different tick rates. For runs 11-16, we forced the tick rate of A to vary from 1 to 6, while fixing the tick rate of B and C to 6. Then, we extrapolated the average logical jump size for A, and created a boxplot to show the typical values this took on.

This logic is contained in the `graph_stats.py` file. Note it's intended to be fed input from runs where B and C had fixed ticks, and A was allowed to vary.

## Varying Internal Event Probability

To generate data for these experiments (21-23) we simply hardcoded different values into the `frame` function and reran the experiment.

## Controlling Difference in Clock Tick

We added support to hardcode the clock ticks for different machines which allowed us to study results when the clock ticks are similar vs when they are very different.
