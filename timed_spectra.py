#!/usr/bin/python3
# import matplotlib       # For remote use
# matplotlib.use('Agg')   # For remote use
import mim, os
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
from scipy.signal.windows import gaussian
from contextlib import ExitStack

# root = os.getcwd()
root = '../absorb_spec/'
fpaths = [root+a for a in sorted(os.listdir(root)) if '.csv' in a]

## Set and apply wavelength range
wl1, wl2 = 550, 800
wavs = np.genfromtxt(fpaths[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)

## Generate reflection spectra
refl = (np.genfromtxt(fpath, delimiter=';',skip_header=33+i1, max_rows=i2-i1,
    unpack=True, usecols=1) for fpath in fpaths)

## Grab peak wavelength for each reflection spectrum
popt_0 = [650, 60, 0.05, 0]
wavs = wavs[i1:i2]
fit_mim_wl = [opt.leastsq(mim.l_residuals, popt_0, args=(wavs, r))[0][0]
    for r in refl]

## Grab timestamp from each file
with ExitStack() as stack:
    open_files = (stack.enter_context(open(fpath)) for fpath in fpaths)
    t = [mim.timestamp(open_file) for open_file in open_files]

# Start from t=0
t = t-np.min(t)

peak_wl_output = np.vstack((t, fit_mim_wl)).T
np.savetxt(root+'peak_wls.txt', peak_wl_output,
    delimiter='\t',
    header='time(min)\t\t\tpeak wavelength (nm)')
