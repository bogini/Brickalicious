#include <Servo.h> 
#include <LiquidCrystal.h>

LiquidCrystal lcd(7,6,5,4,3,2);
 
Servo headRotation;
Servo headCam;

volatile int lastTime; 
volatile long unsigned lastUpdate;

int opID = 0;
int messageInfo = 0;

void setup() { 
  headRotation.attach(9);  
  headCam.attach(8);
  Serial.begin(57600);
  lcd.begin(16,2);
  lcd.setCursor(0,0);
  Serial.flush();
  
  // Get the first time
  lastTime = millis();
  
  lcd.setCursor(0,0);
  lcd.print("Waiting...");
} 

void loop() {
  while (Serial.available() > 0) {
    // Message ID
    opID = serReadInt(); 
    
    delay(1500);
    
    // Message
    messageInfo = serReadInt();
    
    switch (opID) {
      case 1: // Push down cam
              lcd.setCursor(0,0);
              lcd.print("Pushing down");
              lcd.setCursor(0,1);
              lcd.print("head...");
              pushDown();
              delay(1000);
              break;
      case 2: // Move cam up
              lcd.setCursor(0,0);
              lcd.print("Moving cam up...");
              goUp();
              delay(1000);
              break;
      case 3: // Rotate head horizontally
              lcd.setCursor(0,0);
              lcd.print("Rotating head horizontally...");
              horizontal();
              delay(1000);
              break;
      case 4: // Rotate head vertically
              lcd.setCursor(0,0);
              lcd.print("Rotating head");
              lcd.setCursor(0,1);
              lcd.print("vertically...");
              vertical();
              delay(1000);
              break;
      case 5: // Move X
              lcd.setCursor(0,0);
              lcd.print("Moving ");
              lcd.print(messageInfo);
              lcd.setCursor(0,1);
              lcd.print("steps on X...");
              moveStepper(1, messageInfo);
              delay(1000);
              break;
      case 6: // Move Y
              lcd.setCursor(0,0);
              lcd.print("Moving ");
              lcd.print(messageInfo);
              lcd.setCursor(0,1);
              lcd.print("steps on Y...");
              moveStepper(2, messageInfo);
              delay(1000);
              break;
      case 7: // Move Z
              lcd.setCursor(0,0);
              lcd.print("Moving ");
              lcd.print(messageInfo);
              lcd.setCursor(0,1);
              lcd.print("steps on Z...");
              moveStepper(2, messageInfo);
              delay(1000);
              break;
    }
    
    sendConfirmation(opID);
  }
}

int serReadInt() {
   int i, serAva;                           // i is a counter, serAva hold number of serial available
   char inputBytes [7];                 // Array hold input bytes
   char * inputBytesPtr = &inputBytes[0];  // Pointer to the first element of the array
     
   if (Serial.available() > 0) {
     delay(5);                              // Delay for terminal to finish transmitted
                                              // 5mS work great for 9600 baud (increase this number for slower baud)
     serAva = Serial.available();  // Read number of input bytes
     for (i=0; i<serAva; i++) {
         inputBytes[i] = Serial.read();
       }
     
     inputBytes[i] =  '\0';             // Put NULL character at the end
     return atoi(inputBytesPtr);    // Call atoi function and return result
   } else {
       return -1;                           // Return -1 if there is no input
   }
}

void sendConfirmation(int messageId) {
  Serial.println(messageId);
}

void moveStepper(int axis,int amount) {
  if (amount < 0) {
    // Move backwards
  } else if (amount > 0) {
    // Move forward
   
  } 
}

void horizontal() {
  int rotationDegrees = 38;
  headRotation.write(rotationDegrees);
}

void vertical() {
  int rotationDegrees = 138;
  headRotation.write(rotationDegrees);
}

void pushDown() {
  int camAngle = 32;
  headCam.write(camAngle);
}

void goUp() {
  int camAngle = 0;
  headCam.write(camAngle);
}
