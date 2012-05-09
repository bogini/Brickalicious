import os
import sys
import re
import unicodedata
import operator

import Printer
import Communicator

from xml.dom.minidom import parseString
from operator import attrgetter

PUSH_DOWN_CAM = 1
MOVE_CAM_UP   = 2
ROTATE_HEAD_E = 3 # Horizontal (East-West)
ROTATE_HEAD_N = 4 # Vertical (North-South)
MOVE_X        = 5
MOVE_Y        = 6
MOVE_Z        = 7

CARTRIDGE_X = -1
CARTRIDGE_Y = 0
CARTRIDGE_Z = 0

class Pin:
    """
    The pin class represents each pin in the grid system of the base
    
    Attributes: 
        X position
        Y position
        X position
    """
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        
    def __str__(self):
        return "Pin @ (" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"
        
class Brick:
    """
    The brick class represents each brick being put down or that has
    already been placed. It is composed of pins.
    
    Attributes:
        Pin (the origin pin)
        Orientation
        designID
        Covers (a dictionary of all of the pins covered by the brick)
    """
    def __init__(self, x, y, z, orientation, designID):
        self.orientation = orientation
        pin_x = (x-.4)/.8
        pin_y = (y-.4)/.8
        self.pin = Pin(pin_x, pin_y, z/.96)
        self.designID = designID
        self.covering()
        
    def __str__(self):
        return "Brick (" + str(self.designID) + "): " + str(self.orientation) + ", Origin: " + self.pin.__str__()
    
    def valid(self):
        """
        Determines if the brick is a valid 4x2 brick that our printer can 
        work with.
        """
        if self.designID != '3001':
            # Only accept 2x4
            print "The brick was not a 4x2"
            return false
        if self.x > 10 | self.x < -10:
            return false
        if self.y > 10 | self.y < -10:
            return false
        return true
     
    def covering(self):
        """
        Creates a list of all the pins covered by the brick.
        """
        self.covers = []
        if self.orientation == 'N':
            for i in range(4):
                for j in range(2):
                    self.covers.append(Pin(int(self.pin.x) + i, int(self.pin.y) - j, int(self.pin.z)))
        elif self.orientation == 'E':
            for i in range(2):
                for j in range(4):
                    self.covers.append(Pin(int(self.pin.x) + i, int(self.pin.y) + j - 1, int(self.pin.z)))

def parsing(infilename):
    """
    Takes in the lxfml file generated by the user and parses it to identify
    all of the bricks and positions created in the LDD program
    """
    lines = []
    if infilename != "" and os.path.isfile(infilename):
        infile = open(infilename)
        lines = infile.read()
        infile.close()
    else:
        print "FATAL: no input lxfml file has been specified"
        return
    
    bricks = []

    dom = parseString(lines)
    elements = dom.getElementsByTagName('Brick')
    
    for element in elements:
        element = element.toxml()
        
        # designID
        regexp = re.search('designID="...."', element)
        if regexp:
            regexp = regexp.group(0)
            designID = regexp.replace('Brick refID= designID=','').replace('"','')
            
        # Transformation
        regexp = re.search('transformation=".*"', element)
        if regexp:
            regexp = regexp.group(0)
            transformation = regexp.replace('transformation=','').replace('"','')
            
            transformation_array = transformation.split(',')
            orientation = []
            for i in range(9):
                orientation.append(int(round(float(transformation_array[i]), 1)))
            
            position = []
            for i in range(3):
                position.append(round(float(transformation_array[-(i+1)]), 2))
            
            # Orientation
            if orientation == [-1,0,0,0,1,0,0,0,-1]:
                position[2] -= 2.4  # x
                position[0] += 0.8  # y
                orientation = 'N'
            elif orientation == [1,0,0,0,1,0,0,0,1]:
                orientation = 'N'
            elif orientation == [0,0,-1,0,1,0,1,0,0]:
                orientation = 'E'
            elif orientation == [0,0,1,0,1,0,-1,0,0]:
                position[2] += 0.8  # x
                position[0] += 2.4  # y
                orientation = 'E'
                
            # Coordinates
            x = position[2]
            y = position[0]
            z = position[1]
                    
        # Add the brick to the list
        bricks.append(Brick(x, y, z, orientation, designID))
    
    return bricks              
  
def translation(bricks):
    """
    moves the structure so that it is positioned closest to the origin
    """
    low_x = bricks[0].pin.x
    low_y = bricks[0].pin.y
    for brick in bricks:
        if brick.pin.x < low_x:
            low_x = brick.pin.x
        if brick.pin.y < low_y:
            low_y = brick.pin.y
    for brick in bricks:
        brick.pin.x -= low_x
        brick.pin.y -= low_y
        # adding 1 because of the way the LDD origin pin works
        brick.pin.y += 1
        brick.covering()

def generate_build_order(bricks):
    """
    sorts the bricks by x and then y positions, creating a build order
    the moves up each x position, placing bricks
    """
    bricks_ordered = sorted(bricks, key=attrgetter('pin.z', 'pin.x', 'pin.y'))
    return bricks_ordered

def main():
    infilename = "Lego_test.LXFML"
    
    bricks = parsing(infilename)
    translation(bricks)
    build_order = generate_build_order(bricks)
    
    for brick in build_order:
        print brick
    
    # Communication
    #com =  Communicator.Communicator()                    
    #com.setup_connection()
    
    build_list = generate_build_list(build_order)
    
    for foo in build_list:
        #com.send_message(foo[0], foo[1])      
        print foo[0], foo[1]
    
if __name__ == "__main__":
    main()