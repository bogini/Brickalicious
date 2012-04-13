// Cam

#include <Servo.h> 
 
Servo headRotation;
Servo headCam;
 
int pos = 0;
int pos2 = 0;
 
void setup() 
{ 
  headRotation.attach(9);  
  headCam.attach(8);
  Serial.begin(9600);
} 
 
 
void loop() 
{
  //horizontal();
  //pushDown();
  headCam.write(0);
  delay(1000);
  headCam.write(10);
  //vertical();
  //goUp();
  delay(1000);
}

void horizontal() {
  pos = 38;
  headRotation.write(pos);   // 28 = 0º
}

void vertical() {
  pos = 138;
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
