import numpy as np
import matplotlib.pyplot as plt

# Генератор шума
# Белый, синий, фиолетовый, красный, розовый
# 
# N - продолжительность шумового сигнала
# noise_std - стандартное отклонение шумового сигнала
# 
# СПМ - спектральная плотность мощности
#
# white_noise - белый шум - СПМ ~ 1
# blue_noise - голубой шум - СПМ ~ f
# violet_noise - фиолетовый шум - СПМ ~ f^2
# brownian_noise - красный шум - СПМ ~ 1/f^2
# pink_noise - розовый шум - СПМ ~ 1/f
# 
# plot_noise - вывод сгенерированного шума
# plot_spectrum - вывод спектра шума
# plot_spectrum_log - вывод логарифмированного спектра шума

class NOISE:
    def __init__(self):
        pass

    def NOISEGenerator(func):
        @classmethod
        def noise_psd(cls, N, noise_std, dtype=[float, int]):
            X_white = np.fft.rfft(np.random.normal(0, noise_std, N))
            S = func(cls, np.fft.rfftfreq(N))
            # Нормализация S
            S = S / np.sqrt(np.mean(S**2))
            X_shaped = X_white * S
            Y = np.fft.irfft(X_shaped)
                
            if (dtype == int):
                Y = list(map(int, Y))
            
            return Y
        return noise_psd

    @classmethod
    @NOISEGenerator
    def white_noise(cls, f):
        return 1

    @classmethod
    @NOISEGenerator
    def blue_noise(cls, f):
        return np.sqrt(f)

    @classmethod
    @NOISEGenerator
    def violet_noise(cls, f):
        return f

    @classmethod
    @NOISEGenerator
    def brownian_noise(cls, f):
        return 1/np.where(f == 0, float('inf'), f)

    @classmethod
    @NOISEGenerator
    def pink_noise(cls, f):
        return 1/np.where(f == 0, float('inf'), np.sqrt(f))


    @classmethod
    def plot_noise(cls, s, color='#aaaaaa'):
        plt.figure(figsize=(10, 5))
        plt.title('Сгенерированный шумовой сигнал')
        plt.xlabel('X')
        plt.ylabel('Y')
        return plt.plot(s, color)[0]

    @classmethod
    def plot_spectrum_log(cls, s):
        plt.figure(figsize=(10, 5))
        plt.title('Log спектр шума')
        plt.xlabel('freq')
        plt.ylabel('spectrum')
        f = np.fft.rfftfreq(len(s))
        return plt.loglog(f, np.abs(np.fft.rfft(s)))[0]

    @classmethod
    def plot_spectrum(cls, s):
        plt.figure(figsize=(10, 5))
        plt.title('Спектр шума')
        plt.xlabel('freq')
        plt.ylabel('spectrum')
        f = np.fft.rfftfreq(len(s))
        return plt.plot(f, np.abs(np.fft.rfft(s)))[0]



# def noise_psd(N, noise_std, dtype=[float, int], psd = lambda f: 1):
#     X_white = np.fft.rfft(np.random.normal(0, noise_std, N))
#     S = psd(np.fft.rfftfreq(N))
#     # Нормализация S
#     S = S / np.sqrt(np.mean(S**2))
#     X_shaped = X_white * S
#     Y = np.fft.irfft(X_shaped)
        
#     if (dtype == int):
#         Y = list(map(int, Y))
#     return Y
    
# def NOISEGenerator(f):
#     return lambda N, noise_std, dtype=[float, int]: noise_psd(N, noise_std, dtype, f)

# def NOISEGenerator(func):
#     def noise_psd(self, N, noise_std, dtype=[float, int], psd=func):
#         X_white = np.fft.rfft(np.random.normal(0, noise_std, N))
#         S = psd(np.fft.rfftfreq(N))
#         # Нормализация S
#         S = S / np.sqrt(np.mean(S**2))
#         X_shaped = X_white * S
#         Y = np.fft.irfft(X_shaped)
            
#         if (dtype == int):
#             Y = list(map(int, Y))
        
#         return Y
#     return noise_psd

# @NOISEGenerator
# def white_noise(f):
#     return 1

# @NOISEGenerator
# def blue_noise(f):
#     return np.sqrt(f)

# @NOISEGenerator
# def violet_noise(f):
#     return f

# @NOISEGenerator
# def brownian_noise(f):
#     return 1/np.where(f == 0, float('inf'), f)

# @NOISEGenerator
# def pink_noise(f):
#     return 1/np.where(f == 0, float('inf'), np.sqrt(f))


# def plot_spectrum_log(s):
#     f = np.fft.rfftfreq(len(s))
#     return plt.loglog(f, np.abs(np.fft.rfft(s)))[0]

# def plot_spectrum(s):
#     f = np.fft.rfftfreq(len(s))
#     return plt.plot(f, np.abs(np.fft.rfft(s)))[0]

# def plot_noise(s):
#     plt.figure(figsize=(10, 5))
#     plt.title('Сгенерированный шумовой сигнал')
#     plt.xlabel('X')
#     plt.ylabel('Y')
#     return plt.plot(s, color='blue')[0]



# def new_noise(target):
#     def NOISEGenerator(func):
#         @classmethod
#         def noise_psd(cls, N, noise_std, dtype=[float, int], psd=func):
#             X_white = np.fft.rfft(np.random.normal(0, noise_std, N))
#             S = psd(cls, np.fft.rfftfreq(N))
#             # Нормализация S
#             S = S / np.sqrt(np.mean(S**2))
#             X_shaped = X_white * S
#             Y = np.fft.irfft(X_shaped)
                
#             if (dtype == int):
#                 Y = list(map(int, Y))
            
#             return Y
#         return noise_psd
        
#     # def NOISEGenerator(f):
#     #     return lambda N, noise_std, dtype=[float, int]: noise_psd(N, noise_std, dtype, f)

#     @classmethod
#     @NOISEGenerator
#     def white_noise(cls, f):
#         print("white_noise")
#         return 1

#     @classmethod
#     @NOISEGenerator
#     def blue_noise(cls, f):
#         print("blue_noise")
#         return np.sqrt(cls, f)

#     @classmethod
#     @NOISEGenerator
#     def violet_noise(cls, f):
#         print("violet_noise")
#         return f

#     @classmethod
#     @NOISEGenerator
#     def brownian_noise(cls, f):
#         print("brownian_noise")
#         return 1/np.where(f == 0, float('inf'), f)

#     @classmethod
#     @NOISEGenerator
#     def pink_noise(cls, f):
#         return 1/np.where(f == 0, float('inf'), np.sqrt(f))


#     @classmethod
#     def plot_spectrum_log(cls, s):
#         f = np.fft.rfftfreq(len(s))
#         return plt.loglog(f, np.abs(np.fft.rfft(s)))[0]

#     @classmethod
#     def plot_spectrum(cls, s):
#         f = np.fft.rfftfreq(len(s))
#         return plt.plot(f, np.abs(np.fft.rfft(s)))[0]

#     @classmethod
#     def plot_noise(cls, s):
#         plt.figure(figsize=(10, 5))
#         plt.title('Сгенерированный шумовой сигнал')
#         plt.xlabel('X')
#         plt.ylabel('Y')
#         return plt.plot(s, color='blue')[0]


#     target.white_noise = white_noise
#     target.blue_noise = blue_noise
#     target.violet_noise = violet_noise
#     target.brownian_noise = brownian_noise
#     target.pink_noise = pink_noise
#     target.plot_spectrum_log = plot_spectrum_log
#     target.plot_spectrum = plot_spectrum
#     target.plot_noise = plot_noise

#     return target

# @new_noise
# class NOISE:
#     def __init__(self):
#         pass
    

