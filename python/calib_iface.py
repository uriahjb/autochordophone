#!/usr/bin/env python
'''
  Note calibration interface, detects notes, errors to desired notes and 
  what not
'''
import pyaudio
from pylab import *
from time import time as now
from struct import unpack

DEBUG = True

# Notes
notes_seq = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
BASE_FRQ = 261.6 

class NoteCalibration:

  @classmethod
  def frq2note( cls, frq ):
    return 12*log2( frq/BASE_FRQ )

  @classmethod
  def note2frq( cls, note ):
    return pow(2, note/12)*BASE_FRQ
  
  @classmethod
  def note2ind( cls, note_str ):
    return notes_seq.index(note_str)

  def __init__( self, chunk=44100/8, frequency_thresh=750, fftmag_thresh=0.45, alpha=0.25, visual=True ):
    self.chunk = chunk
    self.frequency_thresh = frequency_thresh
    self.fftmag_thresh = fftmag_thresh
    self.visual = visual
    self.alpha = alpha
    self.p = pyaudio.PyAudio()
    self.stream = self.p.open(format=pyaudio.paFloat32,
		    channels=1,
		    rate=44100,
		    input=True,
		    output=True)

    self.n_samples = arange(chunk) 
    self.data = zeros(chunk)

    # fft settings
    self.n_samples = arange(self.chunk)
    self.n_samples2 = range(chunk/2)
    self.sampling_rate = 44100.0
    self.T = chunk/self.sampling_rate
    self.frq = self.n_samples/self.T # two sides frequency range
    self.frq = self.frq[self.n_samples2] # one side frequency range
    self.sample = 0

    self.current_note = None

    if self.visual:
      self.max_fft_val = 0.0
      self.min_fft_val = 0.0

      self.line, = plot( self.n_samples, self.data )
      axis( [min(self.frq), self.frequency_thresh, self.max_fft_val, self.min_fft_val] )
      ion()

  def update( self ):
    new_data = self.stream.read( self.chunk )
    new_data = unpack( self.chunk*'f', new_data )
    new_samples = xrange( self.sample, self.sample+self.chunk )
    #data.append( new_data )
    #n_samples.append( new_samples )
    fft_dat = fft( new_data )/self.chunk
    fft_dat = fft_dat[self.n_samples2]

    inds = argsort( fft_dat )
    sorted_frqs = self.frq[inds]

    sorted_frqs = sorted_frqs[ abs(fft_dat[inds]) > self.fftmag_thresh ]
    sorted_frqs = sorted_frqs[sorted_frqs < self.frequency_thresh]

    

    if self.visual:
      self.max_fft_val = max( max(fft_dat), self.max_fft_val )
      axis( [min(self.frq), self.frequency_thresh, self.min_fft_val, self.max_fft_val] )

    notes_flt = filter( lambda x: isinf(x)!=True, map(self.frq2note, sorted_frqs[:5]))
    idx = map(int, map(round, notes_flt))


    # Run simple low-pass on current note
    if len(notes_flt) > 0:
      if self.current_note is None:
	self.current_note = notes_flt[0]
      else:
	self.current_note = self.alpha*notes_flt[0] + (1.0 - self.alpha)*self.current_note
  
    if DEBUG:
      print 'max_freqs: ', sorted_frqs[:5]
      print 'notes_flt', notes_flt
      print 'notes: ', map( lambda x: notes_seq[mod(x, len(notes_seq))], idx )
      print 'ideal_note' , 
      print 'current_note: ', self.current_note

    self.sample += self.chunk
    if self.visual:
      self.line.set_xdata( self.frq )
      self.line.set_ydata( abs(fft_dat) )
      draw()

if __name__ == '__main__':
  nc = NoteCalibration()
  while True:
    nc.update()

