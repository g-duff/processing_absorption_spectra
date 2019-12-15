#!/usr/bin/python3
# import matplotlib       # For remote use
# matplotlib.use('Agg')   # For remote use
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
from scipy.signal.windows import gaussian
import mim, os

# root = os.getcwd()
root = '../absorb_spec/'
fpaths = [root+a for a in sorted(os.listdir(root)) if '.csv' in a]
num_files = len(fpaths)

## Set and apply wavelength range
wl1, wl2 = 550, 800
wavs = np.genfromtxt(fpaths[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)

## Create wavelength range and peak wavelength lists
t, max_mim_wl, fit_mim_wl = [], [], []
wavs = wavs[i1:i2]

## Add a preview graphs here


## Starting guess
popt_0 = [650, 60, 0.05, 0]

for fpath in fpaths:

    refl = np.genfromtxt(fpath, delimiter=';',
        skip_header=33+i1, max_rows=i2-i1, unpack=True, usecols=1)

    ## Find max wavelength
    max_wl = wavs[np.argmin(refl)]
    max_mim_wl.append(max_wl)
    popt_0[0] = max_wl

    # Fit a Lorentz curve
    popt = opt.leastsq(mim.l_residuals, popt_0, args=(wavs, refl))[0]
    fit_mim_wl.append(popt[0])

    ## Grab timestamp from inside file
    with open(fpath) as open_file:
        t.append(mim.timestamp(open_file))

    print("Completion: " + str(int((i/num_files) *100))+'%', end='\r')

# Start from t=0
t = t-np.min(t)

peak_wl_output = np.vstack((t, max_mim_wl, fit_mim_wl)).T
np.savetxt(root+'peak_wls.txt', peak_wl_output,
    delimiter='\t',
    header='time(min)\t\t\tMax wavelength (nm)\t\t\tpeak wavelength (nm)')
