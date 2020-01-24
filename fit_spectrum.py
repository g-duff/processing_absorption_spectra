import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig
from scipy.signal.windows import gaussian
import numpy.random as rand
import mim

wl1, wl2 = 600, 750

root = './'
fname = 'eg_spec.csv'
wavs, refl = np.genfromtxt(root+fname, delimiter=';', skip_header=33,
    skip_footer=1, unpack=True, usecols=(0,1))

## Low-pass
g_wind = gaussian(len(wavs), 3)
g_wind = g_wind/sum(g_wind)
lp_refl = np.convolve(refl, g_wind, mode='same')

## Truncate for fit
i1, i2 = np.argmin((wavs-wl1)**2), np.argmin((wavs-wl2)**2)
refl_err = 0.05

try:
    print('Fitting with default guess...')
    lorentz_params = [650, 60, 0.05, 0]
    fit_results = opt.curve_fit(mim.lorentz, wavs[i1:i2], refl[i1:i2],
        lorentz_params, refl_err*np.ones(i2-i1), method='lm',
        absolute_sigma=True,)
    lorentz_params = fit_results[0]
    lorentz_errs = np.sqrt(np.diag(fit_results[1]))
except:
    print('Fitting with random guesses')
    # Choose random numbers for fits
    rand_pwl = [rand.choice(wavs[i1:i2]) for i in range(20)]
    popt = [np.concatenate((np.array([p]), rand.rand(3))) for p in rand_pwl]

    fano_fit = [opt.least_squares(mim.l_residuals, p,
        args=(wavs[i1:i2], refl[i1:i2])) for p in popt]

    # Select lowest residuals
    residuals = [f.cost for f in fano_fit]
    popt = [f.x for f in fano_fit]
    lorentz_params = popt[np.argmin(residuals)]

    # Perform fit with lowest-residual parameters
    fit_results = opt.curve_fit(mim.lorentz, wavs[i1:i2], refl[i1:i2],
        lorentz_params, refl_err*np.ones(i2-i1), method='lm',
        absolute_sigma=True,)
    lorentz_params = fit_results[0]
    lorentz_errs = np.sqrt(np.diag(fit_results[1]))

param_names = ('Peak', 'Width', 'Amp', 'Offset')
for p in zip(param_names, lorentz_params, lorentz_errs):
    print('{}\t: {} +/ {}'.format(*p))

fig, ax = plt.subplots()
ax.plot(wavs, refl, 'C4', label='Spectrum', alpha=0.7)
ax.plot(wavs, lp_refl, 'C0', label='Low-pass')
ax.plot(wavs, mim.lorentz(wavs, *lorentz_params), 'C1--', label='Lorentz fit')
ax.axvline(wl1, ls='--', lw=2, color='black')
ax.axvline(wl2, ls='--', lw=2, color='black')
ax.set_xlim([500,1000])
ax.set_ylim(np.mean(refl)+[-0.3,+0.1])
ax = mim.make_spectrum(ax)
plt.savefig(root+'fit_spectrum.png', transparent=True)
plt.show()
