import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

# matplotlib.use('Agg')
font = {'size': 14}
matplotlib.rc('font', **font)

root = os.getcwd()
root = '../absorb_spec/'
t, fit_wl, err_wl = np.genfromtxt(root+'peak_wls.txt', skip_header=1, unpack=True)

fig, ax = plt.subplots()
ax.errorbar(t, fit_wl, yerr=3*err_wl)
ax.grid(True)
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Peak wavelength (nm)')

plt.tight_layout()
fig.savefig(root+'peak_wls.png')
plt.show()
