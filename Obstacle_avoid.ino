#include <Servo.h>

typedef struct MotorDef
{
    Servo   Motor; 
    int     Pin;   // Indicates the Pin this motor is connected to
};

MotorDef Motors;

typedef struct ESCSettingsDef
{
  int Backward;
  int Forward;
  int Stop;
};

ESCSettingsDef ESCSettings; 

int CurrentSpeed;
int Step = 2;


#define ESC_FORW_DEFAULT 200
#define ESC_BACK_DEFAULT 20
#define ESC_STOP 90

#define echoRight 2
#define trigRight 3

#define echoLeft 4
#define trigLeft 5

Servo myservoFront;
Servo myservoBack;

int pos = 0;
/////////////////////////////////////////////////
void setup() {
  Serial.begin(9600);
  Serial.println("Setup: Serial port communication at 9600bps");

  Motors.Pin = 7;
  int pin = Motors.Pin;
  Motors.Motor.attach(pin);

  ESCSettings.Backward = ESC_BACK_DEFAULT; // 20
  ESCSettings.Forward = ESC_FORW_DEFAULT; // 200
  ESCSettings.Stop = ESC_STOP; //90

  pinMode(echoRight, INPUT);
  pinMode(trigRight, OUTPUT);
  pinMode(echoLeft, INPUT);
  pinMode(trigLeft, OUTPUT);

  myservoFront.attach(9);
  myservoBack.attach(10);
  
}

void Run_on_command(){
  //Start with motors still
  Motors.Motor.write(ESCSettings.Stop);

  Serial.println("Running ESC");
  Serial.println("Step = ");
  Serial.print(Step);
  Serial.println("\nPress 'u' to increase speed, 'd' to reduce speed");

  //Set current speed to motors stopped
  CurrentSpeed = ESCSettings.Stop;

  while(1){
    while(!Serial.available())
    {
    }
    char currentChar = Serial.read();
    
    if(currentChar == 'u'){
      Serial.println("\nIncreasing motor speed by step");
      if(CurrentSpeed + Step < ESCSettings.Forward){
        CurrentSpeed = CurrentSpeed + Step;
        Serial.println("New speed = ");
        Serial.print(CurrentSpeed);
      }
      else{
        Serial.println("\nMax speed reaches\n");
      }
    }
    if(currentChar == 'd'){
      Serial.println("\nDecreasing motor speed by step\n");
      if(CurrentSpeed - Step >= ESCSettings.Backward){
        CurrentSpeed = CurrentSpeed - Step;
        Serial.println("New speed = ");
        Serial.print(CurrentSpeed);
      }
      else{
        Serial.println("\nMin speed reached\n");
      }
    }
    if(currentChar == 'e'){
      Serial.println("/nStopping Motors\n");
      CurrentSpeed = ESCSettings.Stop;
    }
    Motors.Motor.write(CurrentSpeed);
  }
  
}

void avoid(){
  int distanceRight;
  int distanceLeft;

  distanceRight = readPingRight();
  distanceLeft = readPingLeft();

  if (distanceRight <= 10 || distanceLeft <= 10){
    moveStop();
    delay(300);
    distanceRight = readPingRight();
    delay(300);
    distanceLeft = readPingLeft();
    delay(300);

    if(distanceRight >= distanceLeft){
      backRight();
      delay(300);
      moveStop();
    }
    else{
      backLeft();
      delay(300);
      moveStop();
    }
  }
  else{
    moveForward();
  }
}

int readPingRight(){
  long duration;
  int distance;

  digitalWrite(trigRight, LOW);
  delayMicroseconds(2);

  digitalWrite(trigRight, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigRight, LOW);

  duration = pulseIn(echoRight, HIGH);
  distance = duration * 0.034/2;

  //Serial.println("Distance_right: ");
  //Serial.println(distance);

  return distance;
}

int readPingLeft(){
  long duration;
  int distance;

  digitalWrite(trigLeft, LOW);
  delayMicroseconds(2);

  digitalWrite(trigLeft, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigLeft, LOW);

  duration = pulseIn(echoLeft, HIGH);
  distance = duration * 0.034/2;

  //Serial.println("Distance_left: ");
  //Serial.println(distance);

  return distance;
}

void moveStop(){
  Motors.Motor.write(90);
  Serial.println("Stop\n");
}

void moveForward(){
  Motors.Motor.write(80);
  myservoBack.write(90);
  Serial.println("Foward\n");
  
}

void moveBackwards(){
  Motors.Motor.write(110);
  Serial.println("Back\n");

}

void backRight(){
  for (pos = 180; pos >= 0; pos -=1){
    myservoBack.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);
  }
  Motors.Motor.write(110);
  Serial.println("backright\n");

}

void backLeft(){
  for (pos = 0; pos <= 180; pos += 1){
    myservoBack.write(pos);
    delay(15);
  }
  Motors.Motor.write(110);
  Serial.println("backleft\n");

}

void loop() {
  //Run_on_command();
  avoid();
}
