import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt
import scipy.signal as sig

# matplotlib.use('Agg') # For remote use
font = {'size': 14}
matplotlib.rc('font', **font)
plt.tight_layout()

root = '/home/george/Desktop/lith_bulk_002/'
pk_wl = np.genfromtxt(root+'peak_wls.txt', usecols=(2), unpack=True,
    skip_header=1)

pk_wl = pk_wl[30:90]

ind = np.arange(0, len(pk_wl), 1)
t = np.arange(0, len(pk_wl), 1)*10/60


plt.plot(t, pk_wl, 'C0.', markersize=2)
plt.grid(True)
plt.xlabel('Time (minutes)')
plt.ylabel('Peak wavelength (nm)')
# plt.ylim([652.3, 653.8])
# plt.savefig('fig_raw_data.png')
plt.show()

i_offset = ind[:100]
pk_wl_offset = pk_wl[:100]

offset = np.polyfit(i_offset, pk_wl_offset, 1)


std = np.std(pk_wl)
mean = np.mean(pk_wl)

plt.plot(t, pk_wl, 'C0.', markersize=4)
plt.plot(t, np.polyval(offset, ind))
plt.grid(True)
plt.xlabel('Time (minutes)')
plt.ylabel('Peak wavelength (nm)')
plt.axhline(mean+std/2, ls='--', color='black', label=f'$\sigma$: {std:1.4f}')
plt.axhline(mean-std/2, ls='--', color='black')
plt.axhline(mean+2*std/2, ls='--', color='red', label=f'2$\sigma$: {2*std:1.4f}')
plt.axhline(mean-2*std/2, ls='--', color='red')
plt.axhline(mean+3*std/2, ls='--', color='green', label=f'3$\sigma$: {3*std:1.4f}')
plt.axhline(mean-3*std/2, ls='--', color='green')
plt.legend()
plt.savefig(root+'fig_noise_poly_offset.png')
plt.show()


pk_wl = pk_wl-np.polyval(offset, ind)
std = np.std(pk_wl)

plt.plot(t, pk_wl, 'C0.', markersize=4)
plt.grid(True)
plt.xlabel('Time (minutes)')
plt.ylabel('Peak wavelength shift (nm)')
plt.axhline(+std/2, ls='--', color='black', label=f'$\sigma$: {std:1.4f}')
plt.axhline(-std/2, ls='--', color='black')
plt.axhline(+2*std/2, ls='--', color='red', label=f'2$\sigma$: {2*std:1.4f}')
plt.axhline(-2*std/2, ls='--', color='red')
plt.axhline(+3*std/2, ls='--', color='green', label=f'3$\sigma$: {3*std:1.4f}')
plt.axhline(-3*std/2, ls='--', color='green')
plt.legend()
plt.savefig(root+'fig_noise_poly_corrected.png')
plt.show()
