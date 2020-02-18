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
fpath = Path('../LED_data/off_sample_through_lens/40db.txt')
index, LED1, LED2, *voltages = loadtxt(fpath, skiprows=1,unpack=True)
voltages = array(voltages)

# Example of how to grab individual channels for stats
# V1 = voltages[:,flatnonzero(LED1)]
# V2 = voltages[:,flatnonzero(LED2)]

# Take mean and standard dev along zero axis
V_mean, V_std = mean(voltages, 0), std(voltages, 0)

# Split into channels
V1 = V_mean[flatnonzero(LED1)]
V2 = V_mean[flatnonzero(LED2)]

# Plot
plt.plot(V1/V2)
plt.tight_layout()
plt.show()
