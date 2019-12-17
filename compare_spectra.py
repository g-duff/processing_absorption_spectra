#!/usr/bin/python3
# import matplotlib       # For remote use
# matplotlib.use('Agg')   # For remote use
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian
import os, mim

## Grab file names
root = '../compare_spec/'
fnames = [a for a in sorted(os.listdir(root)) if '.csv' in a]

## Set and apply wavelength range
wl1, wl2 = 550, 800
wavs = np.genfromtxt(root+fnames[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)
wavs = wavs[i1:i2]

## Create low-pass gaussian window
g_wind = gaussian(len(wavs), 1)
g_wind = g_wind/sum(g_wind)

## Generate refl data, load and low-pass
refl = (np.genfromtxt(root+fname, delimiter=';',skip_header=33, skip_footer=1,
    unpack=True, usecols=1) for fname in fnames)
refl = [np.convolve(r, g_wind, mode='same')[i1:i2] for r in refl]

## Find max, fit Lorentz curve, grab peak and std dev
max_mim_wl = (wavs[np.argmin(r)] for r in refl)
popt_0 = [650, 60, 0.05, 0]
fit_results = [opt.curve_fit(mim.lorentz, wavs, r, popt_0,
    method='lm', absolute_sigma=False) for r in refl]
fit_mim_wl = (r[0][0] for r in fit_results)
mim_wl_std = (np.sqrt(r[1][0,0]) for r in fit_results)

## Format strings for text output
labels = [f.replace('.csv', '').replace('_', ' ') for f in fnames]
peak_wl_output = [pwl[0][:20]+(3*'\t{:1.11f}').format(*pwl[1:])
    for pwl in zip(labels, max_mim_wl, fit_mim_wl, mim_wl_std)]

## Print text output
header = '#Spec name\tMax (nm):\tfit (nm):\tstd (nm):'
print(header)
for pwl in peak_wl_output: print(pwl)

## Write text output to file
with open(root+'outfile.txt', 'w') as outfile:
    outfile.write(header+'\n')
    for pwl in peak_wl_output: outfile.write(pwl+'\n')

## Graphical output
for r, lab in zip(refl, labels): plt.plot(wavs, r, label=lab)
plt.xlabel('Wavelength (nm)')
plt.ylabel('Reflection (normalised)')
plt.legend()
plt.grid(True)
plt.savefig(root+'Compared_spectra.png')
plt.show()
