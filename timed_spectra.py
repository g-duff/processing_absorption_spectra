#!/usr/bin/python3
# import matplotlib       # For remote use
# matplotlib.use('Agg')   # For remote use
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
from scipy.signal.windows import gaussian
import mim
import os

root = os.getcwd()
root = './spec/'
fnames = [a for a in sorted(os.listdir(root)) if '.csv' in a]
num_files = len(fnames)

## Set and apply wavelength range
wl1, wl2 = 500, 800
wavs = np.genfromtxt(root+fnames[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)

## Create low-pass gaussian window
g_wind = sig.windows.gaussian(len(wavs), 1)
g_wind = np.divide(g_wind, sum(g_wind))

## Create wavelength range and peak wavelength lists
t, max_mim_wl, fit_mim_wl = [], [], []
wavs = wavs[i1:i2]

## Add a preview graphs here


## Starting guess
popt_0 = [650, 60, 0.05, 0]

for i, fname in enumerate(fnames):

    refl = np.genfromtxt(root+fname, delimiter=';',
        skip_header=33, skip_footer=1, unpack=True, usecols=1)

    ## Lowpass and truncate
    refl = np.convolve(refl, g_wind, mode='same')
    refl = refl[i1:i2]

    ## Find max wavelength
    max_mim_wl.append(wavs[np.argmin(refl)])

    # Fit a Lorentz curve
    popt = opt.leastsq(mim.l_residuals, popt_0, args =(wavs, refl))[0]
    fit_mim_wl.append(popt[0])

    ## Grab timestamp from inside file
    with open(root+fname) as open_file:
        time_stamp = [open_file.readline() for i in range(4)]
    time_stamp = (time_stamp[3].split(';')[1])[:-1]+'0'

    ## Convert timestamp to minutes and add to our time list, t.
    hr, min, sec, ms = time_stamp[0:2], time_stamp[2:4] , time_stamp[4:6], time_stamp[6:]
    t_minutes = int(hr)*60+(int(min))+(int(sec)/60)
    t.append(t_minutes)

    print("Completion: " + str(int((i/num_files) *100))+'%', end='\r')

# Start from t=0
t = t-np.min(t)

peak_wl_output = np.vstack((t, fit_mim_wl)).T
np.savetxt(root+'peak_wls.txt', peak_wl_output,
    delimiter='\t',
    header='time(min)\t\t\tpeak wavelength (nm)')
