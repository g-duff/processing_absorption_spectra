#!/usr/bin/python3
# import matplotlib       # For remote use
# matplotlib.use('Agg')   # For remote use
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
from scipy.signal.windows import gaussian
import mim

root = os.getcwd()
fnames = [a for a in sorted(os.listdir(root)) if '.csv' in a]

## Set and apply wavelength range
wl1, wl2 = 500, 800
wavs = np.genfromtxt(root+fnames[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)

## Create low-pass gaussian window
g_wind = sig.windows.gaussian(len(wavs), 1)
g_wind = np.divide(g_wind, sum(g_wind))

## Create wavelength range and peak wavelength lists
max_mim_wl, fit_mim_wl = [], []
wavs = wavs[i1:i2]

## Add a preview graphs here


## Starting guess
popt_0 = [650, 60, 0.05, 0]

num_files = len(fnames)
f_indices =  np.arange(0, num_files, 1)

for i in f_indices:

    fname = f'bulk_{i:09d}.csv'
    wavs, refl = np.genfromtxt(fname, delimiter=';',
        skip_header=33, skip_footer=1, unpack=True)

    ## Lowpass and truncate
    refl = np.convolve(refl, g_wind, mode='same')
    refl = refl[i1:i2]

    ## Find max wavelength
    max_mim_wl.append(wavs[np.argmin(refl[i1:i2])])

    # Fit a Lorentz curve
    popt = opt.leastsq(mim.l_lsq, popt_0, args =(wavs[i1:i2], refl[i1:i2]))[0]
    fit_mim_wl.append(popt[0])

t = f_indices*10/60

peak_wl_output = [[i, t[i], fit_mim_wl[i]] for i in f_indices]


np.savetxt(root+'peak_wls.txt', peak_wl_output, header='index, time (min), peak wavelength (nm)')
