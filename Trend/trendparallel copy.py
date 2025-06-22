import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import CubicSpline
import multiprocessing 
import time 

# def f(x):
#     return x*x

# def polinom_trend(time, a=(1,)):
#     if ((type(a) is int) or (type(a) is float)):
#         return [a] * len(time)
    
#     Y = list()
#     for x in time:
#         tDegrees = [(x**i) for i in range(len(a))]
#         Y.append(np.dot(a , tDegrees))
    
#     return Y

# def TRENDGenerator(func):
#     def TRENDpsd(time, **kwargs):
#         with multiprocessing.Pool(3) as p:
#             if len(time) < 1 :
#                 raise TypeError("Необходимо задать кременной промежуток для генерации")
#             print(kwargs)
#             time_seq = np.array_split(time, 3)
#             results = p.map(func, ((time_seq[0], kwargs['a'], kwargs['b']),(time_seq[2], kwargs['a'], kwargs['b']),(time_seq[0], kwargs['a'], kwargs['b'])))
#             print("Result:", results)
#     return TRENDpsd

# @TRENDGenerator
def exp_trend(time, a=1, b=1):
    Y = list()
    for x in time:
        print(x)
        Y.append(a*math.exp(b*x))

    return Y


if __name__ == '__main__':
    t = range(10)
    # exp_trend(time=t, a=2, b=1)
    with multiprocessing.Pool(3) as p:
        if len(t) < 1 :
            raise TypeError("Необходимо задать кременной промежуток для генерации")
        time_seq = np.array_split(t, 3)
        # print(time_seq[0])
        results = p.apply_async(exp_trend, ((time_seq[0],2,2,),(time_seq[1],2,2,),(time_seq[2],2,2,)))
        print("Result:", results.get())
    