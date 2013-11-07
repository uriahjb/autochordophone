from pylab import *
from time import sleep, time as now
from yaml import load
from acp_iface import *

# Load in note to stepper position map
fh = open('tuning.yml', 'r')
note2pos = yaml.load(fh)['note2pos']

iface = Iface( '/dev/ttyACM0' )
stepper = Stepper( iface )
plucker = Servo( 0, iface )
pitch = Servo( 1, iface )

# Set acceleration and vel limits for stepper
stepper.set_limits( 25000, 100, 25000 )

# Set initial positions for servos
plucker.set_position( 0.05 )
pitch.set_position( 0.6 )

mary = ['B', 'A', 'G', 'A', 'B', 'B', 'B',  
	'A', 'A', 'A', 'B', 'D', 'D', 'N',
	'B', 'A', 'G', 'A', 'B', 'B', 'B',
	'B', 'A', 'A', 'B', 'A', 'G', 'N']

# Go to first position
stepper.set_position( note2pos[mary[0]] )
sleep(4.0)
  
pluck_sign = 1

dt = 0.5
cnt = 0
t0 = now()
plucker.set_position( 0.05 * pluck_sign )
pluck_sign *= -1
while True:
  curtime = now()
  # Increment through notes
  if (curtime - t0 > dt):
    t0 = curtime
    if cnt > len(mary)-1:
      cnt = 0
    note = mary[cnt]
    cnt += 1
    if note == 'N':
      continue
    print "idx, %d | note: %s | time: %d" % (cnt-1, note, note2pos[note])
    stepper.set_position( note2pos[note] )
    plucker.set_position( 0.05 * pluck_sign )
    pluck_sign *= -1
  



