from numpy import zeros
from numpy.fft import fft
from numpy.fft import ifft
from numpy.fft import fftshift
from numpy.fft import ifftshift
from numpy import real
import numpy as np
import math

def VME(signal,Alpha,omega_int,fs,tau,tol):
    save_T = len(signal)
    T = save_T
    f_mir = zeros((2*T),dtype=float)
    f_mir[0:T//2:1] = signal[0:T//2:1]
    f_mir[T//2:3*T//2] = signal[::-1]
    f_mir[3*T//2:2*T] = signal[T//2:T:1]
    f = f_mir[::-1]

    T = len(f)
    t = [i/T for i in range(T)]

    eps = np.finfo(float).eps
    udiff = tol + eps

    omega_axis = [i-0.5-1/T for i in t]

    f_hat = fftshift((fft(f)))
    f_hat_onesided = f_hat
    f_hat_onesided[0:T//2] = 0

    N = 500

    omega_d = zeros([N, 1],dtype=complex)
    omega_d[0] = omega_int/fs
    
    lamb = zeros([N, len(omega_axis)],dtype=complex)

    u_hat_d = zeros([N, len(omega_axis)],dtype=complex)

    n = 0

    def count_uhat():
        return (f_hat_onesided[::] +(u_hat_d[n,:]*(Alpha**2)*(omega_axis[::] - omega_d[n,:])**4)+lamb[n,:]/2)/((1+(Alpha**2)*(omega_axis[::] - omega_d[n,:])**4)*(1+2*(Alpha**2)*(omega_axis[::] - omega_d[n,:])**4))
    
    def count_omegad():
        A = np.dot(omega_axis[T//2:T], np.power(np.abs(u_hat_d[n+1, T//2:T]), 2))
        B = np.sum(np.power(np.abs(u_hat_d[n+1, T//2:T]), 2))
        return A/B
        # (omega_axis[T//2:T]*(abs(u_hat_d[n+1, T//2:T])**2).conj().T)/sum(abs(u_hat_d[n+1,T//2:T])**2)
    
    def count_lamb():
        return lamb[n,:] + (tau*(f_hat_onesided-(u_hat_d[n+1,:]+(((Alpha**2)*(omega_axis - omega_d[n+1])**4)*(f_hat_onesided-(u_hat_d[n+1,:])))/(1+2*(Alpha**2)*(omega_axis - omega_d[n+1])**4))))
    
    def count_udiff(udiff):
        return udiff + (1/T)*np.dot((u_hat_d[n,:]-u_hat_d[n-1,:]), np.conj((u_hat_d[n,:]-u_hat_d[n-1,:])))
    

    while(udiff > tol and n < N-1):
    
        u_hat_d[n+1,:] = count_uhat()
    
        omega_d[n+1,0] = count_omegad()
    
        lamb[n+1,:] = count_lamb()
    
        n = n+1

        udiff = count_udiff(udiff)
    
        udiff = np.abs(udiff)


    N = min(N,n) - 1
    omega = omega_d[0:N,:]
    u_hatd = zeros([T, 1],dtype=complex)
    u_hatd[T//2:T,0] = u_hat_d[N,(T//2):T]
    u_hatd[T//2:0:-1,0] = (np.conj(u_hat_d[N,(T//2):T]))
    u_hatd[0,0] = np.conj(u_hatd[-1,0])
    

    u_d = zeros(len(t), dtype=complex)
    u_d[:] = real(ifft(ifftshift(u_hatd[:,0])))
    u_d = u_d[T//4:3*T//4]
    u_hatd = fftshift(fft(u_d[:]))

    return u_d, u_hatd, omega
