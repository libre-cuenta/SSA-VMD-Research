import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import CubicSpline

# Генератор тренда
# полиномиальный, экспоненциальный, экспоненциальный по основанию, логарифмический, степенной, сплайн по точкам
# 
# polinom_trend(a=(1,)) - полиномиальынй тренд - a[0] + a[1]*x + a[2]*x^2 ...
# 
# exp_trend(a, b) - экспоненциальный тренд - a * e^(b*x)
#
# exp2_trend(core, a, b) - экспоненциальный по основанию тренд - a * core^(b*x)
# 
# log_trend(a, b) - логарифмический тренд - a + b*log(c*x)
# 
# spline_trend(x_points, y_points, num_points) - сплайн по точкам
# x_points - x координаты
# y_points - y координаты
# num_points - длина временного ряда
# 
# plot_trend - вывод сгенерированного тренда
# plot_spectrum - вывод спектра тренда
# plot_spectrum_log - вывод логарифмированного спектра тренда

class TREND:
    def __init__(self):
        pass

    def TRENDGenerator(func):
        @classmethod
        def TRENDpsd(cls, time, dtype=[float, int], **kwargs):
            if len(time) < 1 :
                raise TypeError("Необходимо задать кременной промежуток для генерации")
            
            Y = func(cls, time, **kwargs)
            
            if (dtype == int):
                Y = list(map(int, Y))
            
            return Y
        return TRENDpsd

    @classmethod
    @TRENDGenerator
    def polinom_trend(cls, time, a=(1,)):
        if ((type(a) is int) or (type(a) is float)):
            return [a] * len(time)
        
        Y = list()
        for x in time:
            tDegrees = [(x**i) for i in range(len(a))]
            Y.append(np.dot(a , tDegrees))
        
        return Y

    @classmethod
    @TRENDGenerator
    def exp_trend(cls, time, a=1, b=1):
        Y = list()
        for x in time:
            Y.append(a*math.exp(b*x))

        return Y

    @classmethod
    @TRENDGenerator
    def exp2_trend(cls, time, core, a=1, b=1):
        Y = list()
        for x in time:
            Y.append(a * core**(b*x))

        return Y

    @classmethod
    @TRENDGenerator
    def log_trend(cls, time, a=1, b=1, c=1):
        Y = list()
        time_positive = filter(lambda x: x > 0, time)

        for x in time_positive:
            Y.append(a+b*np.log(c*x))

        return Y

    @classmethod
    @TRENDGenerator
    def extend_trend(cls, time, a=1, b=1):
        Y = list()
        for x in time:
            Y.append(a*(x**b))

        return Y

    @classmethod
    def spline_trend(cls, x_points, y_points, num_points=100):
        if len(x_points) != len(y_points):
            raise ValueError("Количество x и y координат должно совпадать")
        
        if len(x_points) < 3:
            raise ValueError("Для построения кубического сплайна необходимо минимум 3 точки")
        
        cs = CubicSpline(x_points, y_points)
        
        x_new = np.linspace(min(x_points), max(x_points), num_points)
        y_new = cs(x_new)
        
        return x_new, y_new


    @classmethod
    def plot_trend(cls, x, s, color='#0000ff'):
        plt.figure(figsize=(10, 5))
        plt.title('Сгенерированный тренд')
        plt.xlabel('X')
        plt.ylabel('Y')
        return plt.plot(x, s, color)[0]

    @classmethod
    def plot_spectrum_log(cls, s):
        plt.figure(figsize=(10, 5))
        plt.title('Log спектр тренда')
        plt.xlabel('freq')
        plt.ylabel('spectrum')
        f = np.fft.rfftfreq(len(s))
        return plt.loglog(f, np.abs(np.fft.rfft(s)))[0]

    @classmethod
    def plot_spectrum(cls, s):
        plt.figure(figsize=(10, 5))
        plt.title('Спектр тренда')
        plt.xlabel('freq')
        plt.ylabel('spectrum')
        f = np.fft.rfftfreq(len(s))
        return plt.plot(f, np.abs(np.fft.rfft(s)))[0]



# def TRENDGenerator(f):
#     def TRENDpsd(time, dtype=[float, int], **kwargs):
#         if len(time) < 1 :
#             raise TypeError("Необходимо задать кременной промежуток для генерации")
        
#         Y = f(time, **kwargs)
        
#         if (dtype == int):
#             Y = list(map(int, Y))
        
#         return Y
#     return TRENDpsd

# @TRENDGenerator
# def polinom_trend(time, a=(1,)):
#     if ((type(a) is int) or (type(a) is float)):
#         return [a] * len(time)
    
#     Y = list()
#     for x in time:
#         tDegrees = [(x**i) for i in range(len(a))]
#         Y.append(np.dot(a , tDegrees))
    
#     return Y

# @TRENDGenerator
# def exp_trend(time, a=1, b=1):
#     Y = list()
#     for x in time:
#         Y.append(a*math.exp(b*x))

#     return Y

# @TRENDGenerator
# def exp2_trend(time, core, a=1, b=1):
#     Y = list()
#     for x in time:
#         Y.append(a * core**(b*x))

#     return Y

# @TRENDGenerator
# def log_trend(time, a=1, b=1):
#     Y = list()
#     time_positive = filter(lambda x: x > 0, time)

#     for x in time_positive:
#         Y.append(a+b*np.log(x))

#     return Y

# @TRENDGenerator
# def extend_trend(time, a=1, b=1):
#     Y = list()
#     for x in time:
#         Y.append(a*(x**b))

#     return Y


# def spline_trend(x_points, y_points, num_points=100):
#     if len(x_points) != len(y_points):
#         raise ValueError("Количество x и y координат должно совпадать")
    
#     if len(x_points) < 3:
#         raise ValueError("Для построения кубического сплайна необходимо минимум 3 точки")
    
#     cs = CubicSpline(x_points, y_points)
    

#     x_new = np.linspace(min(x_points), max(x_points), num_points)
#     y_new = cs(x_new)
    
#     return x_new, y_new