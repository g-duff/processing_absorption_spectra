# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
import os


root = os.getcwd()
root = '/run/user/1000/gvfs/smb-share:server=storage.its.york.ac.uk,share=physics/krauss/George/Optical measurements/19-11-13_bad_bulk/'
ind, t, pk_wl = np.genfromtxt(root+'peak_wls.txt', skip_header=1, unpack=True)

plt.plot(t, pk_wl, 'C0.', markersize=2)
plt.grid(True)
plt.xlabel('Time (minutes)')
plt.ylabel('Peak wavelength (nm)')
plt.savefig(root+'peak_wls.png')
plt.show()
