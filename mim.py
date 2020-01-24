# import matplotlib.pyplot as plt

def fano(x, a1, b1, c1, A1, e):
    eps1 = 2*(x-a1)/b1
    f1 = (eps1+c1)**2/(eps1**2+1)
    y = 1-e-A1*f1
    return y

def lorentz(x, a1, b1, A1, e):
    eps1 = 2*(x-a1)/b1
    f1 = eps1**2/(eps1**2+1)
    y = e+A1*f1
    return y

def f_residuals(params, x, y_meas):
    y_fan = fano(x, *params)
    ressq = y_fan-y_meas
    return ressq

def l_residuals(params, x, y_meas):
    y_fan = lorentz(x, *params)
    ressq = y_fan-y_meas
    return ressq

def timestamp(file):
    ''' Grabs timestamp from an open .csv CCS spectrum file'''
    time_stamp = [file.readline() for i in range(4)]
    time_stamp = (time_stamp[3].split(';')[1])[:-1]+'0'

    ## Convert timestamp to minutes and add to our time list, t.
    if len(time_stamp) == 9:
        hr, min = time_stamp[0:2], time_stamp[2:4]
        sec = time_stamp[4:6]
    elif len(time_stamp) == 8:
        hr, min = time_stamp[0:1], time_stamp[1:3]
        sec = time_stamp[3:5]
    t_minutes = int(hr)*60+int(min)+int(sec)/60
    return t_minutes

def make_spectrum(ax):
    ax.grid(True)
    ax.set_xlabel('Peak wavelength (nm)')
    ax.set_ylabel('Reflection (normalised)')
    ax.legend()
    return ax
