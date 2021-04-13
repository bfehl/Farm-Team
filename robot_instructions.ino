const int pwm_right = 2; 
const int inA_right = A4; 
const int inB_right = A3; 
//
const int pwm_left = 3; 
const int inA_left = 6; 
const int inB_left = 5; 
//
int data = 0;

void setup() {
  Serial.begin(9600);
  pinMode(pwm_right, OUTPUT);
  pinMode(inA_right,OUTPUT);
  pinMode(inB_right,OUTPUT);
  
  pinMode(pwm_left, OUTPUT);
  pinMode(inA_left,OUTPUT);
  pinMode(inB_left,OUTPUT);
}

void loop() {
  if (Serial.available() > 0);{
    data = Serial.read();
    Serial.print(data);
    if (data == '0'){
      //brake
      digitalWrite(inA_left,LOW);
      digitalWrite(inB_left,LOW);
      
      digitalWrite(inA_right,LOW);
      digitalWrite(inB_right,LOW);
      delay(1000);
    }
    if (data == '1'){
       // go forwards
      digitalWrite(inA_left, LOW);
      digitalWrite(inB_left, HIGH);
      analogWrite(pwm_left, 200);
    
      digitalWrite(inA_right, HIGH);
      digitalWrite(inB_right, LOW);
      analogWrite(pwm_right, 200);
    }
    if (data == '2'){
      //turn left
      digitalWrite(inA_right,HIGH);
      digitalWrite(inB_right, LOW);
      analogWrite(pwm_right, 200);

      digitalWrite(inA_left,LOW);
      digitalWrite(inB_left, LOW);
      analogWrite(pwm_left, 200);
      
    }
    if (data =='3'){
      //turn right
      digitalWrite(inA_left, LOW);
      digitalWrite(inB_left, HIGH);
      analogWrite(pwm_left, 200);


      digitalWrite(inA_right, LOW);
      digitalWrite(inB_right, LOW);
      analogWrite(pwm_right, 200);
    }
    if (data=='4'){
      //go backwards
      digitalWrite(inA_left, HIGH);
      digitalWrite(inB_left, LOW);
      analogWrite(pwm_left, 200);
    
      digitalWrite(inA_right, LOW);
      digitalWrite(inB_right, HIGH);
      analogWrite(pwm_right, 200);
    }
  }
}
