import wave                          # opening wav files
import numpy as np                   # general numerical processing 
from scipy import signal as sg       # signal processing 
from matplotlib import pyplot as plt # plotting 
import sys                           # for input arguments

fileName = sys.argv[1]
wavFile = wave.open(fileName) # open the file

# audio info
sampWidth = wavFile.getsampwidth() # number of bytes per sample
nFrames   = wavFile.getnframes()  # number of samples in recording
nChannels = wavFile.getnchannels()  # number of channels (should be 1)
Fs        = wavFile.getframerate()

print('byte width: ', sampWidth)
print('channels:   ', nChannels)
print('sample Rate:', Fs)

if sampWidth == 2:
    sampleType = np.int16
elif sampWidth == 4:
    sampleType = np.float32
else:
    print("Unsupported Audio Format!")
    quit()

#get samples 
samples = np.frombuffer(wavFile.readframes(nFrames),dtype = sampleType).reshape(nFrames,nChannels)
if nChannels > 1:
    samples = samples[:,0] # take the first channels only

#downsample for better low frequency resolution

ds = 4

samples = samples[::ds]
Fs = Fs/ds
#spectrogram
frequency, time, magnitude = sg.spectrogram(samples, Fs) #look at the frequency content over time

magnitude = 10* np.log10(magnitude) # log scale?

# plotting 
plt.pcolormesh(time, frequency, magnitude)
plt.ylabel('Frequency (Hz)')
plt.xlabel('Time (s)')

plt.show()

    
