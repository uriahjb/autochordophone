#!/usr/bin/env python

import pyaudio
from pylab import *
from time import time as now
from struct import unpack, pack

# Initialize pyaudio streamer 
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                output=True)


# Set up a quick filter
# Cutoff frequency of 0.05 Hz
'''
num_samples = 1024
cutoff = 0.0005/(0.5*num_samples)
N = 1024
a = 1
b = signal.firwin( N, cutoff=cutoff)
'''
stream.read(2**16)

chunk = 32
print 'Stream started'
try:
  while True:
    raw = stream.read( chunk )
    data = unpack( chunk*'f', raw )
    #data = signal.lfilter( b, a, data )
    raw_output = pack( chunk*'f', *data )
    stream.write( raw_output )
except KeyboardInterrupt:
  print 'Closing stream'
  stream.close()

