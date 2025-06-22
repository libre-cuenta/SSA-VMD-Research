import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import CubicSpline
import types

# Генератор сезонной компоненты
# Периодическая, почти периодическая, квазипереодическая, псевдопереодическая
# 
# trigonometric_row_1(time, a, b, c, d) - тригонометрический ряд вида - a*|sin(b*x+c)|^d * sign(sin(b*x+c))
# trigonometric_row_2(time, a0, a, b, alpha, delta) - тригонометрический ряд вида - a0 + Sum(i от 1 до N): [a[i]*cos(alpha*i*(x^delta)) + b[i]*sin(alpha*i*(x^delta))]
# frequency_function_sin(time, a0, a, alpha) - поличастотная функция sin - Sum(i от 1 до N): a[i] * sin(alpha[i]*x)
# frequency_function_cos(time, a0, a, alpha) - поличастотная функция cos - Sum(i от 1 до N): a[i] * cos(alpha[i]*x)
# variable_amplitude(time, f(x), b, c) - псевдопериодическая функция с изменяющейся амплитудов - f(x)*sin(b*x+c)
# furier_row(time, c, lamb) - обобщенный ряд Фурье - Sum(i от 1 до N): c[i]*exp^(j*x*lamb[i])
# moduling_signal(time, a0, f) - модулированный сигнал вида - (a0 + sin(f*x))*sin(x)
# moduling_signal2(time, alpha=1, beta=1) - модулированный сигнал вида - sin(alpha*x)*cos(beta*x)
# weierstrass(time, N, alpha=1, beta=1) - Функция Вейерштрасса - Sum(i от 1 до N): (alpha^i) * np.cos( (beta^i)*Pi*x )
# LFM(time, a0, phi0, f0, b) - линейная частотная модуляция - a0 * cos( phi0 + 2*Pi*(f0*t + (b/2)*t^2) )

# plot_season - вывод сгенерированного сезона
# plot_spectrum - вывод спектра сезона
# plot_spectrum_log - вывод логарифмированного спектра сезона


class SEASON:
    def __init__(self):
        pass

    def SEASONGenerator(func):
        @classmethod
        def SEASONpsd(cls, time, dtype=[float, int], **kwargs):
            if len(time) < 1:
                raise TypeError("Необходимо задать кременной промежуток для генерации")
            
            Y = func(cls, time, **kwargs)
            
            if (dtype == int):
                Y = list(map(int, Y))
            
            return Y
        return SEASONpsd
    
    @classmethod
    @SEASONGenerator
    def trigonometric_row_1(cls, time, a=1, b=1, c=0, d=1):
        Y = list()
        for x in time:
            Y.append( a * (np.abs(np.sin(b*x+c)))**(d) * np.sign(np.sin(b*x+c)) )
            
        return Y

    @classmethod
    @SEASONGenerator
    def trigonometric_row_2(cls, time, a0=0, a=(1,), b=(1,), alpha=1, delta=1):
        Y = list()
        if ((type(a) == int or type(a) == float) and (type(b) == int or type(b) == float)):
            for x in time:
                Y.append(a0 + a*np.cos(alpha*(x**delta)) + b*np.sin(alpha*(x**delta)))
            return Y
        try:
            if (type(a) == int or type(a) == float) and len(b)==1:
                for x in time:
                    Y.append(a0 + a*np.cos(alpha*(x**delta)) + b[0]*np.sin(alpha*(x**delta)))
                return Y
        except TypeError:
            pass
        try:
            if len(a)==1 and (type(b) == int or type(b) == float):
                for x in time:
                    Y.append(a0 + a[0]*np.cos(alpha*(x**delta)) + b*np.sin(alpha*(x**delta)))
                return Y
        except TypeError:
            pass
        if (len(a) == 1 or len(b) == 1):
            for x in time:
                season = 0
                for a_i in range(len(a)):
                    for b_i in range(len(b)):
                        season += a[a_i]*np.cos(alpha*(max(a_i, b_i)+1)*(x**delta)) + b[b_i]*np.sin(alpha*(max(a_i, b_i)+1)*(x**delta))
                Y.append(a0 + season)
            return Y

        
        # Проверка входных данных
        if len(a) != len(b):
            raise ValueError("Количество x и y координат должно совпадать")
        for x in time:
            season = 0
            for i in range(len(a)):
                season += a[i]*np.cos(alpha*(i+1)*(x**delta)) + b[i]*np.sin(alpha*(i+1)*(x**delta))
            Y.append(a0 + season)
        return Y
    
    @classmethod
    @SEASONGenerator
    def frequency_function_sin(cls, time, a0=1, a=(1,), alpha=(1,)):
        Y = list()
        if (type(a) == int or type(a) == float) and (type(alpha) == int or type(alpha) == float):
            for x in time:
                Y.append(a0 + a*np.sin(alpha*x))
            return Y
        if type(alpha) == int or type(alpha) == float:
            for x in time:
                season = 0
                for a_i in range(len(a)):
                    season +=a[a_i]*np.sin(alpha*x)
                Y.append(a0 + season)
            return Y
        if type(a) == int or type(a) == float:
            for x in time:
                season = 0
                for alpha_i in range(len(alpha)):
                    season += a * np.sin(alpha[alpha_i]*x)
                Y.append(a0 + season)
            return Y
        if (len(a) == 1 or len(alpha) == 1):
            for x in time:
                season = 0
                for a_i in range(len(a)):
                    for alpha_i in range(len(alpha)):
                        season += a[a_i] * np.sin(alpha[alpha_i]*x)
                Y.append(a0 + season)
            return Y


        # Проверка входных данных
        if len(a) != len(alpha):
            raise ValueError("Количество x и y координат должно совпадать")
        for x in time:
            season = 0
            for i in range(len(a)):
                season += a[i] * np.sin(alpha[i]*x)
            Y.append(a0 + season)

        return Y

    @classmethod
    @SEASONGenerator
    def variable_amplitude(cls, time, f = lambda t: t, b=1, c=1):
        if not ((type(b) == int or type(b) == float) and (type(c) == int or type(c) == float) and (type(f) == types.FunctionType)):
            raise ValueError("Неправильный тип данных f(x), b и c")
        
        Y = list()
        for x in time:
            Y.append(f(x)*np.sin(b*x+c))

        return Y

    @classmethod
    @SEASONGenerator
    def frequency_function_cos(cls, time, a0=1, a=(1,), alpha=(1,)):
        Y = list()
        if (type(a) == int or type(a) == float) and (type(alpha) == int or type(alpha) == float):
            season = 0
            for x in time:
                Y.append(a0 + a*np.cos(alpha*x))
            return Y
        if type(alpha) == int or type(alpha) == float:
            for x in time:
                season = 0
                for a_i in range(len(a)):
                    season +=a[a_i]*np.cos(alpha*x)
                Y.append(a0 + season)
            return Y
        if type(a) == int or type(a) == float:
            for x in time:
                season = 0
                for alpha_i in range(len(alpha)):
                    season += a * np.cos(alpha[alpha_i]*x)
                Y.append(a0 + season)
            return Y
        if (len(a) == 1 or len(alpha) == 1):
            for x in time:
                season = 0
                for a_i in range(len(a)):
                    for alpha_i in range(len(alpha)):
                        season += a[a_i] * np.cos(alpha[alpha_i]*x)
                Y.append(a0 + season)
            return Y


        # Проверка входных данных
        if len(a) != len(alpha):
            raise ValueError("Количество x и y координат должно совпадать")
        for x in time:
            season = 0
            for i in range(len(a)):
                season += a[i] * np.cos(alpha[i]*x)
            Y.append(a0 + season)

        return Y

    @classmethod
    @SEASONGenerator
    def furier_row(cls, time, c=(1,), lamb=(1,)):
        Y = list()
        if ((type(c) == int or type(c) == float) and (type(lamb) == int or type(lamb) == float)):
            for x in time:
                Y.append(np.abs(c*np.exp(complex(0, 1)*x*lamb)))
            return Y
        try:
            if (len(c)==1 and (type(lamb) == int or type(lamb) == float)):
                for x in time:
                    Y.append(np.abs(c[0]*np.exp(complex(0, 1)*x*lamb)))
                return Y
        except TypeError:
            pass
        try:
            if ((type(c) == int or type(c) == float) and len(lamb)==1):
                for x in time:
                    Y.append(np.abs(c*np.exp(complex(0, 1)*x*lamb[0])))
                return Y
        except TypeError:
            pass
        if (len(c) == 1 or len(lamb) == 1):
            for x in time:
                season = 0
                for c_i in range(len(c)):
                    for lamb_i in range(len(lamb)):
                        season += c[c_i]*np.exp(complex(0, 1)*x*lamb[lamb_i])
                Y.append(np.abs(season))
            return Y


        # Проверка входных данных
        if len(c) != len(lamb):
            raise ValueError("Количество x и y координат должно совпадать")
        for x in time:
            season = 0
            for i in range(len(c)):
                season += c[i]*np.exp(complex(0, 1)*x*lamb[i])
            Y.append(np.abs(season))

        return Y

    @classmethod
    @SEASONGenerator
    def moduling_signal(cls, time, a0=1, f=1):
        if not ((type(a0) == int or type(a0) == float) and (type(f) == int or type(f) == float)):
            raise ValueError("Неправильный тип данных a0 и f")

        Y = list()
        for x in time:
            Y.append((a0 + np.sin(f*x))*np.sin(x))
        return Y
    
    @classmethod
    @SEASONGenerator
    def moduling_signal2(cls, time, alpha=1, beta=1):
        if not ((type(alpha) == int or type(alpha) == float) and (type(beta) == int or type(beta) == float)):
            raise ValueError("Неправильный тип данных alpha и beta")

        Y = list()
        for x in time:
            Y.append( np.sin(alpha*x)*np.cos(beta*x) )
        return Y

    @classmethod
    @SEASONGenerator
    def weierstrass(cls, time, N, alpha=1, beta=1):
        # Проверка входных данных
        if not ((type(alpha) == int or type(alpha) == float) and (type(beta) == int or type(beta) == float)):
            raise ValueError("Неправильный тип данных alpha и beta")
        
        Y = list()
        for x in time:
            season = 0
            for i in range(1, N+1):
                season += (alpha**i)*np.cos((beta**i)*np.pi*x)
            Y.append(season)

        return Y
    
    @classmethod
    @SEASONGenerator
    def LFM(cls, time, a0=0, phi0=0, f0=1, b=2):
        # Проверка входных данных
        if not ((type(a0) == int or type(a0) == float) and (type(phi0) == int or type(phi0) == float) \
        and (type(f0) == int or type(f0) == float) and (type(b) == int or type(b) == float)):
            raise ValueError("Неправильный тип данных alpha и beta")
        
        Y = list()
        for x in time:
            Y.append( a0 * np.cos( phi0 + 2*np.pi*(f0*x + (b/2)*x^2) ) )

        return Y
    

    @classmethod
    def plot_season(cls, x, s, color='#fa5500'):
        plt.figure(figsize=(10, 5))
        plt.title('Сгенерированный сезон')
        plt.xlabel('X')
        plt.ylabel('Y')
        return plt.plot(x, s, color)[0]

    @classmethod
    def plot_spectrum_log(cls, s):
        plt.figure(figsize=(10, 5))
        plt.title('Log спектр сезона')
        plt.xlabel('freq')
        plt.ylabel('spectrum')
        f = np.fft.rfftfreq(len(s))
        return plt.loglog(f, np.abs(np.fft.rfft(s)))[0]

    @classmethod
    def plot_spectrum(cls, s):
        plt.figure(figsize=(10, 5))
        plt.title('Спектр сезона')
        plt.xlabel('freq')
        plt.ylabel('spectrum')
        f = np.fft.rfftfreq(len(s))
        return plt.plot(f, np.abs(np.fft.rfft(s)))[0]

