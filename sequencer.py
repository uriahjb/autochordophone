from pylab import *
from acp_iface import *
from time import sleep, time as now
from struct import unpack


# Iface
iface = Iface( '/dev/ttyACM0') 

servo = Servo( iface )
stepper = Stepper( iface )

# Set initial values 
servo.calibrate( 0.00085, 180 )
servo.set_position( 0.2 ) # good servo pos 0.2 - 0.4

stepper.set_limits( 12500, 100, 25000 )

notes = [100, 2000, 2500, 2900, 100]
times = [0, 2.5, 3.0, 4.5, 6.5]

plucks = [0.2, 0.4, 0.2, 0.4, 0.2]
ptimes = [0, 1.2, 1.7, 2.2, 2.7]

t0 = now()
pt0 = now()
cnt = 0
pcnt = 0
while True:
  #cnt = cnt % len(notes) 
  # If cnt > len(notes) reset count and time
  if cnt > len(notes)-1:
    cnt = 0
    t0 = now()

  if pcnt > len(plucks)-1:
    pcnt = 0
    pt0 = now()

  # Increment through notes
  if (now() - t0 > times[cnt]):
    print "idx, %d | note: %d | time: %f" % (cnt, notes[cnt], times[cnt])
    stepper.set_position( notes[cnt] )
    cnt += 1
  
  if (now() - pt0 > ptimes[pcnt]):
    print "idx, %d | pluck: %d | time: %f" % (cnt, plucks[cnt], times[cnt])
    servo.set_position( plucks[pcnt] )
    pcnt += 1



