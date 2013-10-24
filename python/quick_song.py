from pylab import *
from packet_utils import serial_packet
from time import sleep, time as now
from struct import unpack

# Initialize communication interface
sp = serial_packet.SerialPacket( portstr='/dev/ttyACM1' )

# Set up acceleration and velocity limits
accel_lim = 100000
v_min = 100
v_max = 200000
sp.SendPacket(3, [accel_lim, v_min, v_max], 'fff')

notes = [300, 0, -1000, -3000, -3000]
times = [0, 1.5, 2.5, 3.5, 4.5]

t0 = now()
cnt = 0
while True:
  #cnt = cnt % len(notes) 
  # If cnt > len(notes) reset count and time
  if cnt > len(notes)-1:
    cnt = 0
    t0 = now()

  # Increment through notes
  if (now() - t0 > times[cnt]):
    print "idx, %d | note: %d | time: %f" % (cnt, notes[cnt], times[cnt])
    sp.SendPacket(2, [notes[cnt],], 'i')
    cnt += 1
  



