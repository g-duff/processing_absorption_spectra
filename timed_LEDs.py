#!/usr/bin/python3
# import concurrent.futures
from numpy import loadtxt, mean, std, array, flatnonzero
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

# Adjust figure
font = {'size': 14}
matplotlib.rc('font', **font)

# Load data
fpath = Path('/home/gd681/Desktop/bulk_trial/Di_to_15pc_NaCl.txt')
time, LED1, LED2, *voltages = loadtxt(fpath, skiprows=1,unpack=True)
voltages = array(voltages)

time = time[::3]/60 ## Convert to minutes

# Example of how to grab individual channels for stats
# V1 = voltages[:,flatnonzero(LED1)]
# V2 = voltages[:,flatnonzero(LED2)]

# Take mean and standard dev along zero axis
V_mean, V_std = mean(voltages, 0), std(voltages, 0)

# Split into channels
V1 = V_mean[flatnonzero(LED1)]
V2 = V_mean[flatnonzero(LED2)]

plt.plot(time, V1)
plt.plot(time, V2)
plt.show()

# Plot
plt.plot(time, V2/V1)
plt.tight_layout()
plt.show()
