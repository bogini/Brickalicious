// Cam

#include <Servo.h> 
 
Servo headRotation;
Servo headCam;
 
int pos = 0;
int pos2 = 0;
 
void setup() 
{ 
  headRotation.attach(8);  
  headCam.attach(7);
} 
 
 
void loop() 
{
  horizontal();
  pushDown();
  delay(3000);
  vertical();
  goUp();
  delay(3000);
}

void horizontal() {
  pos = 28;
  headRotation.write(pos);   // 28 = 0º
}

void vertical() {
  pos = 115;
  headRotation.write(pos);   // 28 = 0º
}

void pushDown() {
  pos2 = 32;
  headCam.write(pos2);   // 28 = 0º
}

void goUp() {
  pos2 = 0;
  headCam.write(pos2);   // 28 = 0º
}
