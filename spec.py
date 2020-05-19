import wave                          # opening wav files
import numpy as np                   # general numerical processing 
from scipy import signal as sg       # signal processing 
import pyqtgraph as pg               # better plotting
import sys     
from matplotlib import cm            # color maps

fileName = sys.argv[1]
wavFile = wave.open(fileName) # open the file

# audio info
sampWidth = wavFile.getsampwidth() # number of bytes per sample
nFrames   = wavFile.getnframes()   # number of samples in recording
nChannels = wavFile.getnchannels() # number of channels (should be 1)
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
frequency, time, magnitude = sg.spectrogram(samples, Fs, nperseg = 256, noverlap = 128) #look at the frequency content over time

magnitude = 10 * np.log10(magnitude) # log scale?

# plotting
app = pg.QtGui.QApplication([])
glw = pg.GraphicsLayoutWidget()
glw.show()
p = glw.addPlot(0, 0)

img = pg.ImageItem()
p.addItem(img)

# Get the colormap
#colormap = cm.get_cmap("nipy_spectral")  
colormap = cm.get_cmap("CMRmap") 
#colormap = cm.get_cmap("viridis")

colormap._init()
lut = (colormap._lut * 255).view(np.ndarray)  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt

# Apply the colormap
img.setLookupTable(lut) # for input arguments
img.setImage(image = np.transpose(magnitude), levels = (magnitude.min(), 1.01 * magnitude.max()), autoDownsampel = True)

nChunks = len(time)
nFreqs  = len(frequency)

# scale image so axis is correct
img.scale(time[-1] / nChunks , frequency[-1] / nFreqs )

# start event loop for plot
app.exec_()
