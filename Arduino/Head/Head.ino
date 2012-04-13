#include <Servo.h> 
 
Servo headRotation;
Servo headCam;
 
int rotationDegrees = 0;
int camAngle = 0;
int opID = 0;
int messageInfo = 0;
int x = 0;
int y = 0;
int z = 0;

void setup() { 
  headRotation.attach(9);  
  headCam.attach(8);
  Serial.begin(9600);
} 
 
 
void loop() {
  while (Serial.available() > 15) {
    // Message ID
    opID =  Serial.read(); 
    
    // Message
    messageInfo = Serial.read();
    
    switch (opID) {
      case 1: // Push down cam
              pushDown();
              delay(1000);
              break;
      case 2: // Move cam up
              goUp();
              delay(1000);
              break;
      case 3: // Rotate head horizontally
              horizontal();
              delay(1000);
              break;
      case 4: // Rotate head vertically
              vertical();
              delay(1000);
              break;
      case 5: // Move X
              moveStepper(1, messageInfo);
              delay(1000);
              break;
      case 6: // Move Y
              moveStepper(2, messageInfo);
              delay(1000);
              break;
      case 7: // Move Z
              moveStepper(2, messageInfo);
              delay(1000);
              break;
    }
    
    sendConfirmation();
  }
}

void sendConfirmation() {
  Serial.print(1);
}

void moveStepper(axis, amount) {
  if (amount < 0) {
    // Move backwards
  } else if (amount > 0) {
    // Move forwards
   
  } 
}

void horizontal() {
  rotationDegrees = 38;
  headRotation.write(rotationDegrees);
}

void vertical() {
  rotationDegrees = 138;
  headRotation.write(rotationDegrees);
}

void pushDown() {
  camAngle = 32;
  headCam.write(camAngle);
}

void goUp() {
  camAngle = 0;
  headCam.write(camAngle);
}
