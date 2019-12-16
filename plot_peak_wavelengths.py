# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
import os

root = os.getcwd()
root = '../absorb_spec/'
t, fit_wl, err_wl = np.genfromtxt(root+'peak_wls.txt', skip_header=1, unpack=True)

plt.errorbar(t, fit_wl, yerr=3*err_wl)
plt.grid(True)
plt.xlabel('Time (minutes)')
plt.ylabel('Peak wavelength (nm)')
plt.savefig(root+'peak_wls.png')
plt.show()
