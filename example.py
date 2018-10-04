#!/usr/bin/env python
import wave
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import soundfile
FILE_PATCH = "music1.wav"
types = {
    1: np.int8,
    2: np.int16,
    3: np.int32,
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

#Парсим входной wav файл
wav = wave.open(FILE_PATCH, mode="r")
(nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
# nchannels - кол-во каналов
# sampwidth - глубина дискретизации в байтах
# framerate - 
# nframes   - кол-во фреймов
# comptype  - тип компонент
# compname  - имя типа компонент

#Если глубина дискретизации 24 бита
if sampwidth == 3:
    wav.close()
    #Конвертируем в 32 бита
    data, samplerate = soundfile.read(FILE_PATCH)
    soundfile.write('new.wav', data, samplerate, subtype='PCM_32')
    #Открываем и читаем wav заново
    wav = wave.open("new.wav", mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    
# Длительность
duration = nframes / framerate
w, h = 800, 300
# Коэф
k = 50
DPI = 72
# Пиковая амплетуда
peak = 256 ** sampwidth / 2 #sampwidth * 8 * 20 * math.log10(2)    #= 256 ** sampwidth / 2
# Читаем wav  в строку
content = wav.readframes(nframes)
#Приводим к numpy массиву
samples = np.fromstring(content, dtype=types[sampwidth])

plt.figure(1, figsize=(float(w)/DPI, float(h)/DPI), dpi=DPI)
plt.subplots_adjust(wspace=0, hspace=0)

for n in range(nchannels):
    # Отсавляем только эл-ты кратные n + nchannels * p, p in N
    channel = samples[n::nchannels]
    # Отсавляем только эл-ты кратные k * p, p in N
    channel = channel[0::k]

    axes = plt.subplot(2, 1, n+1)
    # Один канал => int8 без знака, отнимаем
    if nchannels == 1:
        channel = channel - peak
        
    # Получили массив диапазонов channel    
    
    

    axes.plot(channel, "g")
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(format_db))
    plt.grid(True, color="w")
    axes.xaxis.set_major_formatter(ticker.NullFormatter())

axes.xaxis.set_major_formatter(ticker.FuncFormatter(format_time))
plt.savefig("wave", dpi=DPI)
plt.show()