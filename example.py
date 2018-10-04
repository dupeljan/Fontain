#!/usr/bin/env python


import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
FILE_PATCH = "24.wav"
types = {
    1: np.int8,
    2: np.int16,
    3: np.dtype([('f', 'i2'), ('l', 'i1')]),
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

def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)

wav = wave.open(FILE_PATCH, mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

duration = nframes / framerate
w, h = 800, 300
k = 50#nframes/w/32
DPI = 72
peak = 256 ** sampwidth / 2 #sampwidth * 8 * 20 * math.log10(2)    #= 256 ** sampwidth / 2
print (sampwidth)
print(peak)
content = wav.readframes(nframes)
'''if sampwidth == 3:
    wav.close()
    wav = wave.open("music.wav", mode="w")
    ###
    wav.setnchannels(nchannels)
    wav.setsampwidth(2)
    wav.setframerate(framerate)
    #wav.writeframes(nframes)
    ###
    wav.close()
    
    wav = wave.open("music.wav", mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    print(nframes)

    print("yooo")
'''
samples = np.fromstring(content, dtype=types[sampwidth])

plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)

for n in range(nchannels):

    channel = samples[n::nchannels]

    channel = channel[0::k]

    axes = plt.subplot(2, 1, n+1)
    
    if sampwidth == 3:
        #Cast type
        file = open("output1",'w')
        new_channel = list()
        for i in range(len(channel) ):
            elem = channel[i]
            res = np.int32( elem["f"] )
            res = res << 8
            res += elem["l"]
            res /
            #print(elem)


            file.write(str(np.asscalar(res)))
            file.write('\n')
            new_channel.append(res) 
        file.close()
        
    
        channel = np.asarray(new_channel)
    
    if nchannels == 1:
        channel = channel - peak
        
    file = open("output",'w')
    for i in range(len(channel)):
        file.write(str(np.asscalar(channel[i])))
        file.write('\n')
    file.close()
    
    

    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()