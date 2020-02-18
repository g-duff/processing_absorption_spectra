#!/usr/bin/python3
import matplotlib
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
import matplotlib.pyplot as plt
from scipy.signal.windows import gaussian
from pathlib import Path
from prettytable import PrettyTable
import mim

# matplotlib.use('Agg')   # For remote use
font = {'size': 14}
matplotlib.rc('font', **font)

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

data_path = Path('../compare_spec')
fpaths = sorted(data_path.glob('*.csv'))

## Set and apply wavelength range
wl1, wl2 = 680, 800
wavs = np.genfromtxt(fpaths[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True, usecols=(0))
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)

## Create low-pass gaussian window
g_wind = gaussian(len(wavs), 10)
g_wind = g_wind/sum(g_wind)

## Generate refl data, load and low-pass
refl = (np.genfromtxt(fp, delimiter=';',skip_header=33, skip_footer=1,
    unpack=True, usecols=1) for fp in fpaths)
refl = [np.convolve(r, g_wind, mode='same') for r in refl]
refl_err = 0.01

## Graphical output
fig, ax = plt.subplots()
labels = [f.name.replace('.csv', '').replace('_', ' ') for f in fpaths]
for r, lab in zip(refl, labels): ax.plot(wavs, r, label=lab)
ax = mim.make_spectrum(ax)
ax.set_xlim([500,1000])
ax.set_ylim([0,1])
# ax.axvline(wl1, ls='--', lw=2, color='black')
# ax.axvline(wl2, ls='--', lw=2, color='black')

plt.tight_layout()
plt.savefig(data_path/'Compared_spectra.png', transparent=True)
plt.show()

## Find max, fit Lorentz curve, grab peak and std dev
max_mim_wl = [wavs[i1+np.argmin(r[i1:i2])] for r in refl]

popt_0 = [max_mim_wl[0], 60, 0.05, 0]
fit_results = [opt.curve_fit(mim.lorentz, wavs[i1:i2], r[i1:i2], popt_0,
    refl_err*np.ones(i2-i1), True, method='lm') for r in refl]
fit_mim_wl = [r[0][0] for r in fit_results]
mim_wl_std = [np.sqrt(r[1][0,0]) for r in fit_results]

header = 'Spec name\tMax (nm)\tfit (nm)\tstd (nm)'
pwl_output = np.vstack((labels, max_mim_wl, fit_mim_wl, mim_wl_std)).T

PT = PrettyTable()
PT.field_names = header.split('\t')
for p in pwl_output: PT.add_row(p)
print(PT)

## Print text output
np.savetxt(data_path/'outfile.txt', pwl_output, header=header, fmt='%s')
