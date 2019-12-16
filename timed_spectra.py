#!/usr/bin/python3
# import concurrent.futures
import mim, os
import numpy as np
import scipy.optimize as opt
from contextlib import ExitStack

# Dashboard
wl1, wl2 = 550, 800
popt_0 = [650, 60, 0.05, 0]
root = '../absorb_spec/'

# Create a list of spectrum files
fpaths = [root+a for a in sorted(os.listdir(root)) if '.csv' in a]

## Set and apply wavelength range using first spectrum file
wavs = np.genfromtxt(fpaths[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)
wavs = wavs[i1:i2]

## Generate reflection data
refl = (np.genfromtxt(fpath, delimiter=';',skip_header=33+i1, max_rows=i2-i1,
    unpack=True, usecols=1) for fpath in fpaths)

## Fit Lorentz curve
fit_results = [opt.curve_fit(mim.lorentz, wavs, r, popt_0,
    method='lm', absolute_sigma=False) for r in refl]
mim_wl = [r[0][0] for r in fit_results]
mim_wl_std = [np.sqrt(r[1][0,0]) for r in fit_results]

## Grab timestamp from each file
with ExitStack() as stack:
    open_files = (stack.enter_context(open(fpath)) for fpath in fpaths)
    t = [mim.timestamp(open_file) for open_file in open_files]

# Start from t=0 then output
t = t-np.min(t)
peak_wl_output = np.vstack((t, mim_wl, mim_wl_std)).T
np.savetxt(root+'peak_wls.txt', peak_wl_output, delimiter='\t',
    header='Time (min)\t\t\tPeak wavelength (nm)\t\tFit stdev (nm)')

## EXAMPLE parallel fitting
# with concurrent.futures.ProcessPoolExecutor() as executor:
#     results = [executor.submit(opt.leastsq, mim.l_residuals, popt_0,
#         args=(wavs, r)) for r in refl]
#     fit_mim_wl = [r.result()[0][0] for r in results]
