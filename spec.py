import wave                          # opening wav files
import numpy as np                   # general numerical processing 
from scipy import signal as sg       # signal processing 
from matplotlib import pyplot as plt # plotting 
import sys                           # for input arguments

fileName = sys.argv[1]
wavFile = wave.open(fileName) # open the file
sampWidth = wavFile.getsampwidth() # 

