#!/usr/bin/env python

from pylab import *
from packet_utils import serial_packet
from time import sleep, time as now
from struct import unpack

sp = serial_packet.SerialPacket( portstr='/dev/ttyACM1' )

data = []
positions = []
speeds = []
times = []


# Set feedback frequency 
sp.SendPacket( 4, [200,], 'H' )

# Set acceleration and velocity limits
sp.SendPacket(3, [2000, 100, 1000], 'fff' )
# Set a desired position
sp.SendPacket(2, [-1000,], 'i')

sample_time = 5.0
t0 = now()
while True:
  if now() - t0 > sample_time:
    # Stop data flood and read it all in
    sp.SendPacket( 4, [0,] , 'H' )
    break
  dat = sp.GetPacketBytes()[1]
  if len(dat) == 0:
    continue
  position, speed, ts = unpack('ffi', dat[1:] )
  positions.append( position )
  speeds.append( speed )
  times.append( ts )
  data.append(dat)


# Flush buffer
while True:
  dat = sp.GetPacketBytes()[1]
  if len(dat) == 0:
    break
