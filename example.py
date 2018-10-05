#!/usr/bin/env python


import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from math import *
import soundfile
FILE_PATCH = "music1.wav"
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
    

def get_db_channel(channel):
	#Create db vector, comput max
	max = 0
	db_chanel = [] 

	for i in range(len(channel)):
		cur = abs(format_db_int(channel[i]))
		db_chanel.append(cur)
		if max < cur:
			max = cur
	# Normalize vector
	if max != 0:
		db_chanel = [ int((i / float(max) ) * 100 ) for i in db_chanel ] 
	
	return	db_chanel

def norm_diferende(channel):
	norm_db = []
	max = 0
	for i in range(len(channel) - 1):
		norm_db.append(abs( channel[i] - channel[i+1]))
		if max < norm_db[i]:
			max = norm_db[i]
	#Normalize
	if max != 0:
		norm_db = [ int((i / float(max) ) * 100 ) for i in norm_db ]
	return norm_db

def write_trigger_points(db_chanel,delt_dur):
	file = open("trigger points.txt",'w')
	abs_dur = 0
	for i in range(len(db_chanel)  -1):
		if db_chanel[i]  > 30:
			new_time = abs_dur 
			#file.write(str(db_chanel[i]))
			#file.write("%.2f"  % abs_dur)
			file.write( "%.2f\tm1:sf(%d)|l3:y\n%.2f\tm1:off" % (new_time ,db_chanel[i]  , new_time + 0.75) )
			file.write('\n')
		abs_dur += delt_dur
	file.close()

def get_frequency(channel, d_time):
    def sign(x):
        if x >= 0:
            return False
        else:
            return True
    freq = []
    begin = 0
    i = 0
    half = False
    cur_time = 0
    while i <  len(channel)  - 1:
        while ( i < len(channel) - 1 and sign(channel[i]) == sign(channel[i+1]) ):
            i += 1
            cur_time +=  d_time
        if not half:
            half = True
            i +=1
        else:
            if cur_time != 0:
                for j in range(begin,i-1):
                    freq.append(int ( (i - begin) / cur_time) )
            begin = i
            half = False
            cur_time = 0
    return freq
            

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

image_nchanel = 1
for n in range(image_nchanel):

    channel = samples[n::nchannels]
    print(len(channel))

    delt_dur = duration / float(len(channel))
    #freq = get_frequency(channel,delt_dur)
    channel = channel[0::k]
    #freq = freq[0::k]
    #for i in range(len(freq)):
    #    print(str(freq[i]))
    


    axes = plt.subplot(2, 1, n+1)

    if nchannels == 1:
        channel = channel - peak
        
    #processing

    delt_dur = duration / float(len(channel)) 
    print(delt_dur )

    #Find time when amplitude diference is large
    
    #Get norm amplitude list 
    db_channel = get_db_channel(channel)
    #Get norm diference
    db_dif = norm_diferende(db_channel)
    #Find trigger poits of time
    write_trigger_points(db_dif,delt_dur)

    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db_str))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()