import numpy as np


def voc_isc(iv_array, area=1.):  #todo: separate V and I
    voc_i = np.where(iv_array[:, 1] == 0)
    if len(voc_i[0]) == 0:
        voc_i = np.where(np.diff(np.sign(iv_array[:, 1])))
    isc_i = np.where(iv_array[:, 0] == 0)
    if len(isc_i[0]) == 0:
        isc_i = np.where(np.diff(np.sign(iv_array[:, 0])))

    voc = iv_array[voc_i, 0]
    isc = iv_array[isc_i, 1]/area

    return voc, isc


def mpp(iv_array, area=1.0):
    power = iv_array[:, 0]*iv_array[:, 1]  # sign issue for current!? wrong mpp,ff values wthout correct sign!
    if np.sign(voc_isc(iv_array)[1][0][0]) == -1:  # array-format correct? Can/should I change it?
        power = iv_array[:, 0]*iv_array[:, 1]*-1
    max_power_idx = np.where(power == np.max(power))
    vpp = iv_array[max_power_idx, 0]
    ipp = iv_array[max_power_idx, 1]/area
    return vpp, ipp


def ff(iv_array):
    fill_factor = mpp(iv_array)[0]*mpp(iv_array)[1]/(voc_isc(iv_array)[0]*voc_isc(iv_array)[1])  # darf ich hier auf vorige Funktionen zurückgreifen?
    return fill_factor


def efficiency(iv_array, area=1.):
    eff = mpp(iv_array)[0]*mpp(iv_array)[1]/area
    # eff = voc_isc(iv_array)[0]*voc_isc(iv_array)[1]/area*ff(iv_array)
    # units?? Pin = 1? # area here if also above??
    return eff


def resistances(iv_array):
    voc_i = np.where(iv_array[:, 1] == 0)
    if len(voc_i[0]) == 0:
        voc_i = np.where(np.diff(np.sign(iv_array[:, 1])))
    isc_i = np.where(iv_array[:, 0] == 0)
    if len(isc_i[0]) == 0:
        isc_i = np.where(np.diff(np.sign(iv_array[:, 0])))

    slope = np.gradient(iv_array[:, 1], iv_array[:, 0])
    rs = 1/slope[voc_i]  # series-resistance: slope at voc point (I=0)
    rsh = 1/slope[isc_i]  # shunt-resistance: slope at isc point (V=0)
    return rs, rsh


data = np.loadtxt("../../iv_data/SG165_small_cell03_long1.txt", skiprows=0, usecols=[0, 1])
print(voc_isc(data))
print(mpp(data))
print(ff(data))
print(efficiency(data, 0.00314))
print(resistances(data))
