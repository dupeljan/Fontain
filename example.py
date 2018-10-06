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

def write_trigger_points(db_chanel,delt_dur,file_name,const):
	file = open(file_name + ".txt",'w')
	abs_dur = 0
	for i in range(len(db_chanel)  -1):
		if db_chanel[i]  > const:
			new_time = abs_dur 
			file.write( "%.2f\tm1:sf(%d)|l3:y\n%.2f\tm1:off" % (new_time ,db_chanel[i]  , new_time + 0.75) )
			file.write('\n')
		abs_dur += delt_dur
	file.close()

def get_freq_channeluency(channel, d_time):
    def sign(x):
        if x >= 0:
            return False
        else:
            return True
    freq_channel = []
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
                    freq_channel.append(int ( (i - begin) / cur_time) )
            begin = i
            half = False
            cur_time = 0
    return freq_channel

def get_elem(param,start_time):
    string = ""
    if param in range(50,100):
        colors = ("c","m","y")
        delta_time = 1.5
        string = "%.2f\tl10:y|m10:sf(15)|m1x1:sf(30)|m1x2:sf(30)|l1x1:r|l1x2:r|m2x1:sf(30)|m2x2:sf(30)|l2x1:c|l2x2:c|m3x1:sf(30)|m3x2:sf(30)|l3x1:m|l3x2:m\n" % start_time
        new_time = start_time + 0.5
        for i in range(1,4):
            string += "%.2f\tm%dx1:sf(100)|m%dx2:sf(100)|l1x1:%s|l1x2:%s|l2x1:%s|l2x2:%s|l3x1:%s" % (new_time,i,i,colors[(i-1) % 3],colors[(i-1) % 3],colors[i % 3],colors[i % 3],colors[(i+1) % 3])
            if i!=1:
                string += "|m%dx1:sf(30)|m%dx2:sf(30)" % (i-1,i-1)
            string += "\n"
            new_time += delta_time
    if param in range(0,50):
        colors = ("g","y","r","b","m","c","m", "w")
        delta_time = 1.5
        string = "%.2f\tl1:g|k6:on|k7:on|k8:on|k9:on|k10:on|k11:on|k12:on|k13:on|k7:chess(20,5)|k8:chess(50,5)|k9:chess(70,5)\n" % start_time
        new_time = start_time + 0.5
        for i in range(1,13):
            string += "%.2f\tm%d:sf(50)|l%d:%s" % (new_time,i,i,colors[(i+1) % 8])
            
            string += "\n"
            new_time += delta_time

    return string

def write_partiture(trigger_vector,delt_dur):
    print(delt_dur)
    file = open("partiture.txt","w")
    for i in range(len(trigger_vector)):
        string = get_elem(trigger_vector[i],i*delt_dur)
        if string != "":
            file.write(string)

    file.close()



         
def normalize_and_dif(vector,file_name,const):
    global duration
    delt_dur = duration / float(len(vector))
    #Get norm diference
    norm_dif_vector = norm_diferende(vector)
    #Find trigger poits of time
    write_trigger_points(norm_dif_vector,delt_dur,file_name,const)
    return norm_dif_vector



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

for n in range(1):

    channel = samples[n::nchannels]
    
    
    
    

    #freq_channel = get_freq_channeluency(channel,delt_dur)
    #freq_channel = freq_channel[0::k]
    #for i in range(len(freq_channel)):
    #    print(str(freq_channel[i]))
    channel = channel[0::k]
    
    delt_dur = duration / float(len(channel))


    axes = plt.subplot(2, 1, n+1)

    if nchannels == 1:
        channel = channel - peak
        
    #processing

    
    #Find time when amplitude diference is large
    
    
    db_channel = get_db_channel(channel)
    amplitude_dif = normalize_and_dif(db_channel,"amplitude",30)
    #frq_dif = normalize_and_dif(freq_channel,"frequency",7)
    write_partiture(amplitude_dif,delt_dur)
    


    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db_str))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()