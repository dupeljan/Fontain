#!/usr/bin/env python


import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import *
import soundfile
FILE_PATCH = "24.wav"
types = {
    1: np.int8,
    2: np.int16,
    3: np.int32,#np.dtype([('f', 'i2'), ('l', 'i1')]),
    4: np.int32
}
def format_time(x, pos=None):
    global duration, nframes, k
    progress = int(x / float(nframes) * duration * k)
    mins, secs = divmod(progress, 60)
    hours, mins = divmod(mins, 60)
    out = "%d:%02d" % (mins, secs)
    if hours > 0:
        out = "%d:" % hours
    return out

def format_db_str(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * log10(abs(x) / float(peak))
    return int(db)

def format_db_int(x):
    global peak
    if x == 0:
        return 0

    db = 20 * log10(abs(x) / float(peak))
    return int(db)
    

wav = wave.open(FILE_PATCH, mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

if sampwidth == 3:
    wav.close()
    data, samplerate = soundfile.read(FILE_PATCH)
    soundfile.write('new.wav', data, samplerate, subtype='PCM_32')
    wav = wave.open("new.wav", mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()



duration = nframes / framerate
w, h = 800, 300
sec_part = 4
k = framerate / sec_part #very 1/sec_part second
DPI = 72
peak = 256 ** sampwidth / 2 #sampwidth * 8 * 20 * math.log10(2)    #= 256 ** sampwidth / 2
content = wav.readframes(nframes)


samples = np.fromstring(content, dtype=types[sampwidth])

plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)

for n in range(nchannels):

    channel = samples[n::nchannels]

    channel = channel[0::k]

    axes = plt.subplot(2, 1, n+1)

    if nchannels == 1:
        channel = channel - peak
        
    #processing

    delt_dur = duration / float(len(channel)) 
    print(delt_dur )
    abs_dur  = 0

    #Find time when amplitude diference is large
    file = open("trigger points" + str(n),'w')
    const_diference = 1
    for i in range(len(channel) - 1):
    	if abs(abs( format_db_int(channel[i]) ) - abs( format_db_int(channel[i+1]) ))   > const_diference:
    		file.write(str(abs_dur))
    		file.write('\n')
    	abs_dur += delt_dur

    file.close()
    

    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db_str))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()