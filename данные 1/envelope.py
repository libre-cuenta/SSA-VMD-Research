import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import CubicSpline

def hl_envelopes_idx(s, dmin=1, dmax=1, split=False):
    """
    Input :
    s: 1d-array, data signal from which to extract high and low envelopes
    dmin, dmax: int, optional, size of chunks, use this if the size of the input signal is too big
    split: bool, optional, if True, split the signal in half along its mean, might help to generate the envelope in some cases
    Output :
    lmin,lmax : high/low envelope idx of input signal s
    """

    # locals min      
    lmin = (np.diff(np.sign(np.diff(s))) > 0).nonzero()[0] + 1 
    # locals max
    lmax = (np.diff(np.sign(np.diff(s))) < 0).nonzero()[0] + 1 
    
    if split:
        # s_mid is zero if s centered around x-axis or more generally mean of signal
        s_mid = np.mean(s) 
        # pre-sorting of locals min based on relative position with respect to s_mid 
        lmin = lmin[s[lmin]<s_mid]
        # pre-sorting of local max based on relative position with respect to s_mid 
        lmax = lmax[s[lmax]>s_mid]

    # global min of dmin-chunks of locals min 
    lmin = lmin[[i+np.argmin(s[lmin[i:i+dmin]]) for i in range(0,len(lmin),dmin)]]
    # global max of dmax-chunks of locals max 
    lmax = lmax[[i+np.argmax(s[lmax[i:i+dmax]]) for i in range(0,len(lmax),dmax)]]
    
    return lmin,lmax


def spline_trend(x_points, y_points, num_points=100):
    if len(x_points) != len(y_points):
        raise ValueError("Количество x и y координат должно совпадать")
    
    if len(x_points) < 3:
        raise ValueError("Для построения кубического сплайна необходимо минимум 3 точки")
    
    cs = CubicSpline(x_points, y_points)
    
    x_new = np.linspace(min(x_points), max(x_points), num_points)
    y_new = cs(x_new)
    
    return x_new, y_new


def spline_envelope(f, dmin=1, dmax=1, split=False):
    lmin, lmax = hl_envelopes_idx(f, dmin, dmax, split)
    num_points = len(f)

    _, high_envelope = spline_trend(lmax, f[lmax], num_points)
    _, low_envelope = spline_trend(lmin, f[lmin], num_points)

    return low_envelope, high_envelope
