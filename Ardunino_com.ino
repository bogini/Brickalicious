#include <Servo.h> 

Servo headRotation;
Servo headCam;

// Distance from the limit switch to the cartdridge
int cDistX = 745;
int cDistY = 2950;
int cDistZ = 1000;

int opID = 0;
int messageInfo = 0;
volatile boolean minimum = false;
volatile boolean maximum = false;

boolean emergency = false;
boolean pickingUp = false;
boolean flag = false;

// Pins
int cwPin = 9;
int clkPin = 10;
int xStepper = 11;
int yStepper = 12;
int zStepper = 13;

int xRange = 8732;
int yRange = 0;
int zRange = 0;

void setup() {
  pinMode(cwPin, OUTPUT);
  pinMode(clkPin, OUTPUT);
  pinMode(xStepper, OUTPUT);
  pinMode(yStepper, OUTPUT);
  pinMode(zStepper, OUTPUT);

  pinMode(A0, OUTPUT); // Red
  pinMode(A1, OUTPUT); // Yellow
  pinMode(A2, OUTPUT); // Green
  
  pinMode(A3, OUTPUT); // X Reset
  pinMode(A4, OUTPUT); // Y Reset
  pinMode(A5, OUTPUT); // Z Reset
  
  digitalWrite(A0, LOW); // Red
  digitalWrite(A1, LOW);  // Yellow
  digitalWrite(A2, HIGH); // Green
  
  headRotation.attach(4);  
  headCam.attach(5);

  Serial.begin(57600);
  Serial.flush();

  attachInterrupt(0, emergencyMode, RISING); // Digital pin 2
  attachInterrupt(1, emergencyMode, RISING); // Digital pin 3
  
  pushDown();  // Make sure there are no bricks when started
  horizontal();
  
}

void emergencyMode() {
  emergency = true;
  
  if (!pickingUp) {
    digitalWrite(A0, HIGH); // Red
    digitalWrite(A1, LOW);  // Yellow
    digitalWrite(A2, LOW); // Green
    
    digitalWrite(clkPin, LOW);
    
    Serial.println(10);
  }
}

void loop() {
  if (!emergency) {
    digitalWrite(A0, LOW); // Red
    digitalWrite(A1, LOW);  // Yellow
    digitalWrite(A2, HIGH); // Green
  } else {
    digitalWrite(A0, HIGH); // Red
    digitalWrite(A1, LOW);  // Yellow
    digitalWrite(A2, LOW); // Green
  }
  
  while (Serial.available() > 0 && !emergency) {
    digitalWrite(A0, LOW); // Red
    digitalWrite(A1, HIGH);  // Yellow
    digitalWrite(A2, LOW); // Green
  
    // Message ID
    opID = serReadInt(); 

    delay(1500);

    // Message
    messageInfo = serReadInt();
    
    pickingUp = false;
    
    switch (opID) {
    case 1: // Push down cam
      
      pushDown();
      break;
    case 2: // Move cam up
      goUp();
      break;
    case 3: // Rotate head horizontally
      horizontal();
      break;
    case 4: // Rotate head vertically
      vertical();
      break;
    case 5: // Move X
      moveStepper(1, messageInfo);
      break;
    case 6: // Move Y
      moveStepper(2, messageInfo);
      break;
    case 7: // Move Z
      moveStepper(3, messageInfo);
      break;
    case 8: //Pick up brick
      //pushDown();  // Make sure there are no bricks when started
      horizontal();
      pickingUp = true;
      moveStepper(3, 400); //Z
      moveStepper(2, 30000); //Y
      while (flag)
        delay(10);
      moveStepper(1, -30000); //X
      while (flag)
        delay(10);
      moveStepper(3, -30000); //Z
      break;
    }
    
    //delay(500);
    
    sendConfirmation(opID);
  }
}

int serReadInt() {
  int i, serAva;                           // i is a counter, serAva hold number of serial available
  char inputBytes [7];                 // Array hold input bytes
  char * inputBytesPtr = &inputBytes[0];  // Pointer to the first element of the array

  if (Serial.available() > 0) {
    delay(5);                              // Delay for terminal to finish transmitted
    // 5mS works great for 9600 baud (increase number for slower baud)
    serAva = Serial.available();  // Read number of input bytes
    for (i=0; i<serAva; i++) {
      inputBytes[i] = Serial.read();
    }

    inputBytes[i] =  '\0';             // Put NULL character at the end
    return atoi(inputBytesPtr);    // Call atoi function and return result
  } 
  else {
    return -1;                           // Return -1 if there is no input
  }
}

void sendConfirmation(int messageId) {
  Serial.println(messageId);
}

void moveStepper(int axis,int amount) {
  flag = true;
  int microsends = 700;
  
  if (!emergency) {
    digitalWrite(A3, LOW); // Reset Pin X
    digitalWrite(xStepper, LOW);
    digitalWrite(A4, LOW); // Reset Pin Y
    digitalWrite(yStepper, LOW);
    digitalWrite(A5, LOW); // Reset Pin Z
    digitalWrite(zStepper, LOW);
  
    if (axis == 1) {
      digitalWrite(A3, HIGH); // Reset Pin X
      digitalWrite(xStepper, HIGH);
    } else if(axis == 2) {
      digitalWrite(A4, HIGH); // Reset Pin Y
      digitalWrite(yStepper, HIGH);
    } else if(axis == 3) {
      digitalWrite(A5, HIGH); // Reset Pin Z
      digitalWrite(zStepper, HIGH);
    }
    
    if (amount < 0) {
      // Move backwards
      digitalWrite(cwPin, HIGH);
      for (int i = 0; i < -amount; i++) {
        if (emergency) {
          Serial.println(i);
          // Go forward
          int foo = 500;
          if (pickingUp) {
            emergency = false;
            if (axis == 1)
              foo += cDistX;
            else if (axis == 2)
              foo += cDistY;
            else if (axis == 3)
              foo += cDistZ;
          }
          digitalWrite(cwPin, LOW);
          for (int i = 0; i < foo; i++) {
            digitalWrite(clkPin, HIGH);
            delayMicroseconds(microsends);
            digitalWrite(clkPin, LOW);
            delayMicroseconds(microsends);
          }
          break;
        }
        digitalWrite(clkPin, HIGH);
        delayMicroseconds(microsends);
        digitalWrite(clkPin, LOW);
        delayMicroseconds(microsends);
      }
    } else if (amount > 0) {
      // Move forward
      digitalWrite(cwPin, LOW);
      for (int i = 0; i < amount; i++) {
        if (emergency) {
          Serial.println(i);
          // Go backwards one step
          int foo = 500;
          if (pickingUp) {
            emergency = false;
            if (axis == 1)
              foo += cDistX;
            else if (axis == 2)
              foo += cDistY;
            else if (axis == 3)
              foo += cDistZ;
          }
          digitalWrite(cwPin, HIGH);
          for (int i = 0; i < foo; i++) {
            digitalWrite(clkPin, HIGH);
            delayMicroseconds(microsends);
            digitalWrite(clkPin, LOW);
            delayMicroseconds(microsends);
          }
          break;
        }
        digitalWrite(clkPin, HIGH);
        delayMicroseconds(microsends);
        digitalWrite(clkPin, LOW);
        delayMicroseconds(microsends);
      }
    }
  }
  
  digitalWrite(A3, LOW); // Reset Pin X
  digitalWrite(xStepper, LOW);
  digitalWrite(A4, LOW); // Reset Pin Y
  digitalWrite(yStepper, LOW);
  digitalWrite(A5, LOW); // Reset Pin Z
  digitalWrite(zStepper, LOW);
    
  if (pickingUp)
    emergency = false;
    
  flag = false;
}

void horizontal() {
  int rotationDegrees = 148;
  headRotation.write(rotationDegrees);
}

void vertical() {
  int rotationDegrees = 49;
  headRotation.write(rotationDegrees);
}

void pushDown() {
  if (!emergency) {
    // Go down
    for(int posX = 110; posX>=80; posX--) {                                
      headCam.write(posX);
      delay(10);
    }
    
    // Go up
    for(int posX = 80; posX<=110; posX++) {                                
      headCam.write(posX);
      delay(5);
    }
    
    moveStepper(3, -90);
    delay(100);
    
    // Go down
    for(int posX = 110; posX>=80; posX--) {                                
      headCam.write(posX);
      delay(10);
    }
    
    // Go up
    for(int posX = 80; posX<=110; posX++) {                                
      headCam.write(posX);
      delay(5);
    }
    
    moveStepper(3, -40);
  }
}

void goUp() {
  int camAngle = 0;
  if (!emergency)
    headCam.write(camAngle);
}
