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

def f_lsq(params, x, y_meas):
    y_fan = fano(x, *params)
    ressq = y_fan-y_meas
    return ressq

def l_lsq(params, x, y_meas):
    y_fan = lorentz(x, *params)
    ressq = y_fan-y_meas
    return ressq
