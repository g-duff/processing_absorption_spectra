#!/usr/bin/python3
from numpy import loadtxt, mean, std, array, flatnonzero
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

# Adjust figure
font = {'size': 14}
matplotlib.rc('font', **font)

# Load data
fpath = Path('/Users/george/Desktop/Di_to_15pc_NaCl.txt')
time, LED1, LED2, *voltages = loadtxt(fpath, skiprows=1, unpack=True)
voltages = array(voltages)

time = time[::3]/60  # Convert to minutes

# Example of how to grab individual channels for stats
# V1 = voltages[:,flatnonzero(LED1)]
# V2 = voltages[:,flatnonzero(LED2)]

# Take mean and standard dev along zero axis
V_mean, V_std = mean(voltages, 0), std(voltages, 0)

# Split into channels
V1 = V_mean[flatnonzero(LED1)]
V2 = V_mean[flatnonzero(LED2)]

# Individual voltages
fig_indiv, (ax1, ax2) = plt.subplots(nrows=2, sharex=True)
ax1.plot(time, V1, 'C0')
ax2.plot(time, V2, 'C1')
ax1.set_ylabel('Voltage (V)')
ax2.set_ylabel('Voltage (V)')
ax2.set_xlabel('Time (minutes)')
ax1.grid(True)
ax2.grid(True)
fig_indiv.tight_layout()

# Voltage ratio
fig_ratio, ax_ratio = plt.subplots()
ax_ratio.plot(time, V2/V1, 'C0')
ax_ratio.set_xlabel('Time (minutes)')
ax_ratio.set_ylabel('Voltage ratio')
ax_ratio.grid(True)
fig_ratio.tight_layout()

plt.show()
