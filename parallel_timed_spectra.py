import concurrent.futures as cf
import numpy as np
import mim
import scipy.optimize as opt
from pathlib import Path
import time

'''
Loading a file takes similar time to fitting a curve
so to reduce the run time, this script fits a curve and loads
the next file simultaneously.

Saves ~1s per 1000 files
'''

###### Consumer function(s) ######

def fit_curve(wavs, refl, popt_0):
    ''' Fitting function'''
    fit_results = opt.curve_fit(mim.lorentz, wavs, refl, popt_0,
                             method='lm', absolute_sigma=False)
    mim_wl = fit_results[0][0]
    mim_wl_std = np.sqrt(fit_results[1][0, 0])

    return mim_wl, mim_wl_std    

# Wavelength range and fit params
wl1, wl2 = 550, 800
popt_0 = [650, 60, 0.05, 0]

# Define file list and preallocate for results
data_path = Path('./test_spectra')
fpaths = sorted(data_path.glob('*.csv'))
Nfiles = len(fpaths)
mim_wl = np.zeros(Nfiles)
mim_wl_std = np.zeros(Nfiles)
t = np.zeros(Nfiles)

# Load first file
wavs, next_file = np.genfromtxt(fpaths[0], delimiter=';',
    skip_header=33, skip_footer=1, unpack=True)

# Truncate to wavelength range
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)
wavs = wavs[i1:i2]
next_file = next_file[i1:i2]

# Timeout of 5 seconds
to = 5

# Loading params
load_file_kwargs = {"delimiter": ';', 
    "skip_header": 33+i1,
    "max_rows": i2-i1,
    "unpack": True,
    "usecols": 1}

###### Producer loop ######
with cf.ProcessPoolExecutor(max_workers=2) as executor:

    for i, fpath in enumerate(fpaths[1:]): # Loop through file names

        # Set next file loading (~0.005s)
        load_next_file = executor.submit(np.genfromtxt, fpath, 
            **load_file_kwargs)

        # Fit curve (~0.003s)
        res = executor.submit(fit_curve, wavs, next_file, popt_0)

        # Grab results
        mim_wl[i], mim_wl_std[i] = res.result(timeout=to)
        next_file = load_next_file.result(timeout=to)

        # Grab timestamp (0.00015s - not submitted because it is FAST)
        with open(fpath) as open_file:
            t[i] = mim.timestamp(open_file)

# Fit the last loaded file and grab its timestamp
mim_wl[-1], mim_wl_std[-1] = fit_curve(wavs, next_file, popt_0)

with open(fpath) as open_file:
    t[-1] = mim.timestamp(open_file)

# Output/save here
t = t-np.min(t)
peak_wl_output = np.vstack((t, mim_wl, mim_wl_std)).T
np.savetxt(data_path/'peak_wls_parallel.txt', peak_wl_output, delimiter='\t',
           header='Time (min)\t\t\tPeak wavelength (nm)\t\tFit stdev (nm)')
