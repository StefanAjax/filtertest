import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write


f1 = 113.0  
f2 = 83.0
cf = 8000

fs = 44100.0 

t = np.arange(0, 1, 1/fs)
f = np.arange(0, fs, 1)

# print(t)
# print(f)
# print(t.size)
# print(f.size)

y1 = np.sin(2*np.pi*f1*t)
y2 = np.sin(2*np.pi*f2*t)

carrier = np.sin(2*np.pi*cf*t)

y = y1 + y2
yf = np.fft.fft(y)
yfabs = np.absolute(yf)

ym = y*carrier
ymf = np.fft.fft(ym)
ymfabs = np.absolute(ymf)

# plot original

fig1 = plt.figure(1)
timeax1 = fig1.add_subplot(2, 1, 1)
freqax1 = fig1.add_subplot(2, 1, 2)

timeax1.plot(t, y)
freqax1.vlines(f, 0, yfabs)
freqax1.plot(f, yfabs, 'ko')
timeax1.set_ylabel('Time')
freqax1.set_ylabel('Frequency')

# plot modulated

fig2 = plt.figure(2)
timeax2 = fig2.add_subplot(2, 1, 1)
freqax2 = fig2.add_subplot(2, 1, 2)

timeax2.plot(t, ym)
freqax2.vlines(f, 0, ymfabs)
freqax2.plot(f, ymfabs, 'ko')
timeax2.set_ylabel('Time')
freqax2.set_ylabel('Frequency')

# print(yfabs[2929:2931])

scaled = np.int16(y/np.max(np.abs(y))*32767)
write('test.wav', 44100, scaled)

plt.show(block=False)

while True:
    print("Skriv: ", end="")
    a = input()
    print(eval(a))