#!/usr/bin/python3
# import concurrent.futures
from numpy import loadtxt, mean, std, array, nonzero
import matplotlib.pyplot as plt
from pathlib import Path

# Load data
fpath = Path('../LED_data/off_sample_through_lens/70db.txt')
index, LED1, LED2, *voltages = loadtxt(fpath, skiprows=1,unpack=True)
voltages = array(voltages)

# Take mean and standard dev
V_mean, V_std = mean(voltages, 0), std(voltages, 0)

# Split into channels
V1 = V_mean[nonzero(LED1)]
V2 = V_mean[nonzero(LED2)]

# Plot
plt.plot(V1/V2)
plt.show()
