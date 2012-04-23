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
  
class Communicator:
  def setup_connection(self):
    port = "/dev/tty.usbmodemfd121"
    self.ser = serial.Serial(port,57600,timeout = 1)  # opens serial port
    print "Connected to " + self.ser.portstr       	# check which port was really used
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
    except:
      #print "Error decoding the confirmation message."
      return False

  def message_info(self, message):
    return str(struct.unpack("!ii", message))

if __name__ == "__main__":                     
  com = Communicator()                           
  com.setup_connection()                         
  
                                                
  com.send_message(PUSH_DOWN_CAM, 0)
  time.sleep(2)            
  com.send_message(MOVE_CAM_UP, 0)  
  time.sleep(2)               
  com.send_message(ROTATE_HEAD_E, 0)
  time.sleep(2)
  com.send_message(ROTATE_HEAD_N, 0)
  time.sleep(2)
  com.send_message(MOVE_X, 23)                   
  time.sleep(2)
  com.send_message(MOVE_Y, 34)   
  time.sleep(2)
  com.send_message(MOVE_Z, 42)                                   
  time.sleep(2)
  com.send_message(MOVE_Z, -22)                  
                                                   
  com.close_connection()                         