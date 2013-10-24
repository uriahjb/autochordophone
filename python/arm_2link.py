#!/usr/bin/env python
import pygame
from pygame.locals import *
from pylab import *
from time import time as now, sleep

DEBUG = False

class Arm_2Link:

  def __init__( self, origin=array([0.0,0.0]), joints=array([0.0,0.0]), links=ones(2), elbow_up=True, color='k' ):
    # Initialize arm parameters
    self.origin = origin
    self.joints = joints
    self.links = links

    self.sign = 1.0
    if elbow_up:
      self.sign = -1.0

    # Initialize plotting environment
    #ion()
    '''
    pts = vstack(( zeros(2)
		    , self.fk()))
    self.links_h, = plot( pts[:,0], pts[:,1], '-'+color )
    hold('true')
    self.joints_h, = plot( pts[:,0], pts[:,1], 'o'+color )
    axis([-3.0, 3.0, -3.0, 3.0])
    grid('on')
    draw()
    '''

  '''
  def draw( self ):
    pts = vstack(( zeros(2)
		    , self.fk()))
    self.links_h.set_xdata( pts[:,0]+self.origin[0] )
    self.links_h.set_ydata( pts[:,1]+self.origin[1] )
    self.joints_h.set_xdata( pts[:,0]+self.origin[0] )
    self.joints_h.set_ydata( pts[:,1]+self.origin[1] )
    draw()
  '''
    
  def set_xy( self, xy_des ):
    print 'xy_des: ', xy_des
    
    self.ik( xy_des - self.origin )

  def fk( self ):
    '''
    given thetas and links compute the endpoints of each link

    zero theta orientation is straight up and down
    '''
    thetas = self.joints
    links = self.links
    t0 = thetas[0]
    pts0 = array([cos(t0)*links[0]
		 ,sin(t0)*links[0]])
    t1 = t0+thetas[1]
    pts1 = array([cos(t1)*links[1]+pts0[0]
		 ,sin(t1)*links[1]+pts0[1]])
    return vstack((pts0,pts1))

  def ik( self, xy_des ):
    '''
    Given a desired xy point and the set of links compute the 
    "upper elbow" inverse kinematics solution

    The solution method is as follows:
      - Solve problem as angles of a triangle where you know the
	lengths of each link
      - Then account for the additional theta between the x axis and triangle hypotenuse for the base joint

    TODO: Still need to account for NaN results from arccos when 
	  no solution exists, for instance when xy_des is too close
	  or too far away
    '''
    l0 = self.links[0]
    l1 = self.links[1]
    l2 = sqrt(sum(pow(xy_des,2)))

    # Get angle between x-axis and triangle hypotenuse ( vector from base to xy_des )
    t0 = arctan2( xy_des[1], xy_des[0] )

    # Angle of j0 as part of triangle
    t1 = arccos( (pow(l0,2)+pow(l2,2)-pow(l1,2))/(2.0*l0*l2) )

    # Solve for j0 and j1
    #j0 = t0 - t1
    j0 = t0 + self.sign*t1
    #j0 = t1
    #j1 = arccos( (pow(l0,2)+pow(l1,2)-pow(l2,2))/(2.0*l0*l1) )
    #j1 = pi - arccos( (pow(l0,2)+pow(l1,2)-pow(l2,2))/(2.0*l0*l1) )
    j1 = pi + self.sign*arccos( (pow(l0,2)+pow(l1,2)-pow(l2,2))/(2.0*l0*l1) )
   
    # Convert j1 such that the angle is relative to my zero axis
    # convention
    #j1 = j1 - pi 
   
    if DEBUG: 
      print 'xy_des', xy_des
      print 'l0: ', l0
      print 'l1: ', l1 
      print 'l2: ', l2
      print 't0: ', t0
      print 't1: ', t1
      print 'j0: ', j0
      print 'j1: ', j1
   
    # Don't update joint values if invalid request is made
    if isnan(j0) or isnan(j1):
      return array([j0, j1])

    self.joints = array([j0, j1])
    return array([j0, j1])


if __name__ == '__main__':
  '''
  Pygame visualization that moves the arm around
  '''
  win_size = (600, 600)
  m2px = 100.0
  pygame.init()
  pygame.display.init()
  screen = pygame.display.set_mode( win_size )
  pygame.display.set_caption( '2Link Arm Demo' )

  draw = pygame.draw

  arm = Arm_2Link()
  arm.set_xy( array([1.0, 1.0]) )

  framerate = 20.0

  captured = False
  eef_pos = array([1.0, 1.0])

  t0 = now()
  while True:

    # Temporal guard
    curtime = now()
    if (curtime - t0) < 1.0/framerate: 
      continue
    t0 = curtime

    # Handle input events
    for evt in pygame.event.get():
      if evt.type == MOUSEBUTTONDOWN:
	if sum(pow(array([evt.pos[0], evt.pos[1]]) - pts[-1,:],2)) < 100:
	  captured = True

      if evt.type == MOUSEMOTION and captured:
	eef_pos = array([(evt.pos[0]-win_size[0]/2)/m2px, (win_size[1]/2-evt.pos[1])/m2px])
	if DEBUG:
	  print eef_pos
  
      if evt.type == MOUSEBUTTONUP:
	captured = False


    screen.fill((0, 0, 0))

    # Compute joint positions
    arm.ik( eef_pos )
  
    # Get joint positions and convert to pixel space
    pts = m2px*vstack( (zeros(2), arm.fk()) ) + array(win_size)/2
    pts[:,1] = win_size[1] - pts[:,1] 

    for i in xrange(0,len(pts)-1):
      p0 = (pts[i,0], pts[i,1])
      p1 = (pts[i+1,0], pts[i+1,1])
      draw.line( screen, (255,255,255), p0, p1 )
      rect_width = 10
      screen.fill( (255,255,255), rect=pygame.Rect( (p0[0]-rect_width/2,p0[1]-rect_width/2, rect_width, rect_width) ))
      if DEBUG:
	print (pts[i,:], pts[i+1,:])

    pygame.display.flip()


    




