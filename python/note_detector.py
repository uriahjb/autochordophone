#!/usr/bin/env python

import pyaudio
from pylab import *
from time import time as now
from struct import unpack

BASE_FRQ = 261.6 

def frq2note( frq ):
  return 12*log2( frq/BASE_FRQ )

def note2frq( note ):
  return pow(2, note/12)*BASE_FRQ

def note2ind( note_str ):
  return notes_seq.index(note_str)

# Notes
notes_seq = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

max_frq = 2000

# Initialize pyaudio streamer 
p = pyaudio.PyAudio()

#chunk = 5*1024
chunk =	44100

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                output=True)

# Set up realtime plotting
ion()

sample = 0
#chunk = 44100
chunk = 44100/8
#chunk = 4096 
#chunk = 1024 
n_samples = arange(chunk) 
data = zeros(chunk)

n_samples2 = range(chunk/2)

sampling_rate = 44100.0
T = chunk/sampling_rate
frq = n_samples/T # two sides frequency range
frq = frq[n_samples2] # one side frequency range

max_fft_val = 0.0
min_fft_val = 0.0

line, = plot( n_samples, data )
axis( [min(frq), max(frq), max_fft_val, min_fft_val] )

current_note = 0.0

while True:
  new_data = stream.read( chunk )
  new_data = unpack( chunk*'f', new_data )
  new_samples = xrange( sample, sample+chunk )
  #data.append( new_data )
  #n_samples.append( new_samples )
  fft_dat = fft( new_data )/chunk
  fft_dat = fft_dat[n_samples2]

  inds = argsort( fft_dat )
  sorted_frqs = frq[inds]

  fft_thresh = 0.45
  sorted_frqs = sorted_frqs[ abs(fft_dat[inds]) > fft_thresh ]
  sorted_frqs = sorted_frqs[sorted_frqs < max_frq]

  print 'max_freqs: ', sorted_frqs[:5]

  max_fft_val = max( max(fft_dat), max_fft_val )
  #min_fft_val = max( min(fft_dat), min_fft_val )
  axis( [min(frq), max_frq, min_fft_val, max_fft_val] )

  notes_flt = filter( lambda x: isinf(x)!=True, map(frq2note, sorted_frqs[:5]))

  idx = map(int, map(round, notes_flt))

  print 'notes_flt', notes_flt
  print 'notes: ', map( lambda x: notes_seq[mod(x, len(notes_seq))], idx )

  # Run simple low-pass on current note
  if len(notes_flt) > 0:
    alpha = 0.25
    current_note = alpha*notes_flt[0] + (1.0 - alpha)*current_note
 
  print 'ideal_note' , 
  print 'current_note: ', current_note
  sample += chunk
  line.set_xdata( frq )
  line.set_ydata( abs(fft_dat) )
  draw()


