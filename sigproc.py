# Kolla upp freqs och butter

import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import butter, lfilter
import pyaudio
import wave
import time


def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


order = 6

f1 = 649.0  
f2 = 400.0
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

ymr = ym*carrier
ymrf = np.fft.fft(ymr)
ymrfabs = np.absolute(ymrf)

fig3 = plt.figure(3)
timeax3 = fig3.add_subplot(2, 1, 1)
freqax3 = fig3.add_subplot(2, 1, 2)

timeax3.plot(t, ymr)
freqax3.vlines(f, 0, ymrfabs)
freqax3.plot(f, ymrfabs, 'ko')
timeax3.set_ylabel('Time')
freqax3.set_ylabel('Frequency')


ymrl = butter_lowpass_filter(ymr, 800, fs, order=5)
ymrlf = np.fft.fft(ymrl)
ymrlfabs = np.absolute(ymrlf)

fig4 = plt.figure(4)
timeax4 = fig4.add_subplot(2, 1, 1)
freqax4 = fig4.add_subplot(2, 1, 2)

timeax4.plot(t, ymrl)
freqax4.vlines(f, 0, ymrlfabs)
freqax4.plot(f, ymrlfabs, 'ko')
timeax4.set_ylabel('Time')
freqax4.set_ylabel('Frequency')

plt.show(block=False)

scaled = np.int16(y/np.max(np.abs(y))*32767)
write('y.wav', 44100, scaled)

scaled = np.int16(ym/np.max(np.abs(ym))*32767)
write('ym.wav', 44100, scaled)

scaled = np.int16(ymr/np.max(np.abs(ymr))*32767)
write('ymr.wav', 44100, scaled)

scaled = np.int16(ymrl/np.max(np.abs(ymrl))*32767)
write('ymrl.wav', 44100, scaled)

chunk = 4096  

# open a wav format music

for i in ["y.wav", "ym.wav", "ymr.wav", "ymrl.wav"]:

    f = wave.open(i, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)
    #
    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()
    time.sleep(2)


eval(input())
