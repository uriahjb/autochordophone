#!/usr/bin/env python
'''
Autochordophone interfaces one for the stepper another 
for the servo 
'''
from packet_utils import serial_packet

class Iface:
  def __init__( self, portstr ):
    self.sp = serial_packet.SerialPacket( portstr )

  def write( self, msg_fmt, data ):
    print msg_fmt[0], data, msg_fmt[1]
    self.sp.SendPacket( msg_fmt[0], data, msg_fmt[1] )

class Stepper:
  '''
  Message Format:
    name : [ id, format ]
  '''  
  _msg_fmt = { 'set_limits' : [ 3, 'fff' ] 
	     , 'set_position' : [ 2, 'i' ] }

  def __init__( self, iface ):
    self.iface = iface
    self.v_min = 0
    self.v_max = 0
    self.accel_limit = 0
    self.position = 0
  
  def set_limits( self, accel, v_min, v_max ):
    '''
    Set Stepper Limits in units of steps:
      - Acceleration
      - Velocity Min
      - Velocity Max
    '''
    self.v_min = v_min
    self.v_max = v_max
    self.accel_limit = accel
    self.iface.write( self._msg_fmt['set_limits'], [accel, v_min, v_max] )

  def set_position( self, position ):
    self.position = position
    self.iface.write( self._msg_fmt['set_position'], [int(position),] )

class Servo:
  _msg_fmt = {'set_position' : [6, 'Bf']
	     ,'calibrate' : [7, 'Bfi'] }

  def __init__( self, id, iface ):
    self.iface = iface
    self.id = id
    self.position = 0 

  def calibrate( self, rng, degrees ):
    self.iface.write( self._msg_fmt['calibrate'], [self.id, rng, int(degrees)] )

  def set_position( self, position ):
    self.iface.write( self._msg_fmt['set_position'], [self.id, position,] )


if __name__ == '__main__':
  # Initialize interface
  iface = Iface( '/dev/ttyACM1' )
  servo = Servo( iface )


