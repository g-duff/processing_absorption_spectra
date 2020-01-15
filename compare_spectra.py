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
# try:
#     import tkinter as tk
#     from tkinter import filedialog as fd
#     root = tk.Tk()
#     root.withdraw()
#     print()
#     data_dir = fd.askdirectory()+'/'
# except ModuleNotFoundError:
#     data_dir = os.getcwd()


data_dir = '/run/user/1000/gvfs/smb-share:server=storage.its.york.ac.uk,\
share=physics/krauss/George/Optical measurements/20-01-14_Surface_sensitivity/sample_002/'
fnames = [a for a in sorted(os.listdir(data_dir)) if '.csv' in a]

print(fnames)

## Set and apply wavelength range
wl1, wl2 = 680, 800
wavs = np.genfromtxt(data_dir+fnames[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)
# wavs = wavs[i1:i2]

## Create low-pass gaussian window
g_wind = gaussian(len(wavs), 10)
g_wind = g_wind/sum(g_wind)

## Generate refl data, load and low-pass
refl = (np.genfromtxt(data_dir+fname, delimiter=';',skip_header=33, skip_footer=1,
    unpack=True, usecols=1) for fname in fnames)
refl = [np.convolve(r, g_wind, mode='same') for r in refl]
refl_err = 0.05

## Graphical output
fig, ax = plt.subplots()
labels = [f.replace('.csv', '').replace('_', ' ') for f in fnames]
for r, lab in zip(refl, labels): ax.plot(wavs, r, label=lab)
ax = mim.make_spectrum(ax)
ax.set_xlim([500,1000])
ax.set_ylim([0.6,1])
# ax.axvline(wl1, ls='--', lw=2, color='black')
# ax.axvline(wl2, ls='--', lw=2, color='black')
plt.savefig(data_dir+'Compared_spectra.png', transparent=True)
plt.show()

## Find max, fit Lorentz curve, grab peak and std dev
max_mim_wl = [wavs[i1+np.argmin(r[i1:i2])] for r in refl]
print(max_mim_wl)


popt_0 = [max_mim_wl[0], 60, 0.05, 0]
fit_results = [opt.curve_fit(mim.lorentz, wavs[i1:i2], r[i1:i2], popt_0,
    refl_err*np.ones(i2-i1), True, method='lm') for r in refl]
fit_mim_wl = (r[0][0] for r in fit_results)
mim_wl_std = (np.sqrt(r[1][0,0]) for r in fit_results)

## Format strings for text output
peak_wl_output = [pwl[0][:20]+(3*'\t{:1.11f}').format(*pwl[1:])
    for pwl in zip(labels, max_mim_wl, fit_mim_wl, mim_wl_std)]

## Print text output
header = '#Spec name\tMax (nm):\tfit (nm):\tstd (nm):'
print(header)
for pwl in peak_wl_output: print(pwl)

## Write text output to file
with open(data_dir+'outfile.txt', 'w') as outfile:
    outfile.write(header+'\n')
    for pwl in peak_wl_output: outfile.write(pwl+'\n')
