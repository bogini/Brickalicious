import serial
import struct
import time

# Packet Types - must match arduino
PUSH_DOWN_CAM = 1
MOVE_CAM_UP   = 2
ROTATE_HEAD_E = 3 # Horizontal (East-West)
ROTATE_HEAD_N = 4 # Vertical (North-South)
MOVE_X        = 5
MOVE_Y        = 6
MOVE_Z        = 7
PICK_BRICK_UP = 8

class Communicator:
  def setup_connection(self):
    port = "/dev/tty.usbmodemfd121"
    #port = "COM4"
    self.ser = serial.Serial(port,57600,timeout = 1)  # opens serial port
    print "Connected to " + self.ser.portstr        # check which port was really used
    time.sleep(2) # necessary to stablish connection
  
  def close_connection(self):
    self.ser.close()
    
  def send_message(self, messageId, data):
    message = struct.pack("!ii", messageId, data)
    print 'Sending ' + self.message_info(message) + '...'
    self.ser.write(str(messageId))
    self.ser.write(",")
    time.sleep(0.5)
    self.ser.write(str(data))
    print "Waiting for confirmation..."
    while 1:                                      # wait until Arduino has sent
      if self.wait_for_confirmation(messageId):  # a confirmation message with the 
        print "Confirmed!"
        break                                    # last messsageId sent
      time.sleep(1)
    
  def wait_for_confirmation(self, flag):
    try:
      data = self.ser.readline()
      confirmation = int(data.strip())
      if confirmation == flag:
        return True
      elif confirmation == 10:
        print "**** EMERGENCY !!! ****"
    except:
      #print "Error decoding the confirmation message."
      return False

  def message_info(self, message):
    return str(struct.unpack("!ii", message))

  def print_bricks(self, brick_list):
        build_list = []
        
        for brick in brick_list:
            #conversion between lego pins and stepper motor steps
            print brick.pin.x, brick.pin.y, brick.pin.z
            x = (brick.pin.y * 632)
            y = -(brick.pin.x * 632)
            z = (brick.pin.z) * 780 
            print x,y,z
            #Move to cartridge and move down to pick up brick
            build_list.append([PICK_BRICK_UP, 0])
            build_list.append([MOVE_Z,z])
            #Orient Head
            xFix = 0
            yFix = 0
            if brick.orientation == 'N':
                build_list.append([ROTATE_HEAD_N,0])
                # Fix so the rotation happens on the center of the brick
                xFix = 632
                yFix = -2 * 632
            # elif brick.orientation == 'E':
            #     build_list.append([ROTATE_HEAD_N,0])
            #Move to origin
            #larger numbers on y mean closer to the limit switch
            build_list.append([MOVE_Y, 2680 + y + yFix])
            build_list.append([MOVE_X, 6480 + x + xFix])
            build_list.append([MOVE_Z, -(1000)])
            #Push brick out
            build_list.append([PUSH_DOWN_CAM, 0])
        
        build_list.append([MOVE_Z, 7000])
        
        return build_list
          
        
if __name__ == "__main__":                     
  com = Communicator()                           
  com.setup_connection()
  while 1:
    com.send_message(MOVE_Z, -8000)
    com.send_message(MOVE_Z, 8000)
                                    
  com.close_connection()                         
