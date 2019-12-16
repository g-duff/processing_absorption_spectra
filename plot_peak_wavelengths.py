# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
import os

root = os.getcwd()
root = '../absorb_spec/'
t, fit_wl = np.genfromtxt(root+'peak_wls.txt', skip_header=1, unpack=True)

plt.plot(t, fit_wl, 'C0.', markersize=2)
plt.grid(True)
plt.xlabel('Time (minutes)')
plt.ylabel('Peak wavelength (nm)')
plt.savefig(root+'peak_wls.png')
plt.show()
