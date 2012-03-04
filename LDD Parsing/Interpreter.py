import os
import sys
import re
import unicodedata

from xml.dom.minidom import parseString

class Brick:
    def __init__(self, x, y, z, orientation, designID):
        self.x = x
        self.y = y
        self.z = z
        self.orientation = orientation
        self.designID = designID
    
    def valid(self):
        # Determines if a brick is valid or not
        if self.designID != '3001':
            # Only accept 2x4
            return false
        if self.x > 10 | self.x < -10:
            return false
        if self.y > 10 | self.y < -10:
            return false
        return true

def main():
    infilename = "Lego_test.LXFML"

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
            designID = regexp.replace('designID=','').replace('"','')
            
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
                orientation = ''
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
            
            print designID +  ':', orientation, '@', x, y, z
        
        # Add the brick to the list
        bricks.append(Brick(x, y, z, orientation, designID))
    
if __name__ == "__main__":
    main()
