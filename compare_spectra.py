#!/usr/bin/python3
# import matplotlib       # For remote use
# matplotlib.use('Agg')   # For remote use
import os
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian
import mim

## Grab file names
root = os.getcwd()
root = './spec/'
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

## Starting guess for Lorentzian fit
popt_0 = [650, 60, 0.05, 0]

for fname in fnames:

    refl = np.genfromtxt(root+fname, delimiter=';',
        skip_header=33, skip_footer=1, unpack=True, usecols=1)

    ## Low pass and truncate
    refl = np.convolve(refl, g_wind, mode='same')
    refl = refl[i1:i2]

    ## Find max wavelength
    max_mim_wl.append(wavs[np.argmin(refl)])

    ## Fit a Lorentz curve
    popt = opt.leastsq(mim.l_residuals, popt_0, args =(wavs, refl))[0]
    fit_mim_wl.append(popt[0])

    ## Plot spectrum with label from filename
    plt.plot(wavs, refl, label = fname.replace('.csv', '').replace('_', ' '))

print(max_mim_wl)
print(fit_mim_wl)

plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflection (normalised)')
plt.legend()
plt.savefig(root+'Compared_spectra.png')
plt.show()
