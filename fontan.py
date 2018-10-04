#!/usr/bin/env pythonpytho



import wave
import numpy as np
import math

types = {
    1: np.int8,
    2: np.int16,
    3: np.dtype([('f', 'i2'), ('l', 'i1')]),
    4: np.int32
}


def format_db(x, pos=None):
    if pos == 0:
        return ""
    global peak
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)

wav = wave.open("music.wav", mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()

duration = nframes / framerate
w, h = 800, 300
k = nframes/w/32
DPI = 72
peak = 256 ** sampwidth / 2

content = wav.readframes(nframes)
samples = np.fromstring(content, dtype=types[sampwidth])


for n in range(nchannels):
    channel = samples[n::nchannels]

    channel = channel[0::k]
    if nchannels == 1:
        channel = channel - peak

    if sampwidth == 3:
    	#Cast type
    	for i in range(len(channel) ):
    		elem = channel[i]
    		res = np.int32( elem["f"] )
    		res = res << 8
    		res += elem["l"]
    		print(elem)
    		print(res)

    '''
    for i in range(len(channel)):
    	print(channel[i])    
   '''