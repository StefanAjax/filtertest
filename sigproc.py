import numpy as np
import matplotlib.pyplot as plt


f1 = 30.0  # Hz, signal frequency
f2 = 70.0
cf = 3000

fs = 44100.0  # Hz, sampling rate (ie. >= 2*f)

t = np.arange(-1, 1+1/fs, 1/fs)

x1 = np.sin(2*np.pi*f1*t)
x2 = np.sin(2*np.pi*f2*t)


carrier = np.sin(2*np.pi*cf*t)


x = x1 + x2
xm = x*carrier
xf = np.fft.fft(xm)

plt.figure(1)
plt.plot(t, xf)

plt.show()

