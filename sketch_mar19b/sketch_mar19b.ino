#include "Arduino_SensorKit.h"

float pressure;
int light_sensor = A3;
int potentiometer = A0;

int LED = 4;
int led8 = 8;
int led3 = 3;
int buzzer = 5;

int passive_algorithm;
 
void setup() {
Serial.begin(9600); //begin Serial Communication

pinMode(LED,OUTPUT);
pinMode(led3,OUTPUT);
pinMode(led8,OUTPUT);
pinMode(potentiometer,INPUT);
pinMode(buzzer,OUTPUT);

passive_algorithm = 0;

Pressure.begin();
}
 
void loop() {
String inputString = Serial.readStringUntil('\n');
  if(inputString=="read"){
      int raw_light = analogRead(light_sensor); // read the raw value from light_sensor pin (A3)
      int wind = map(Pressure.readPressure(), 90000, 110000, 0, 100);
      
      int light = map(raw_light, 0, 1023, 0, 100); // map the value from 0, 1023 to 0, 100
      
      int potentiometer = map(analogRead(potentiometer),0,1023,0,100);
      
      String message = "r-" + String(light) + "-" + String(wind) + "-" + String(potentiometer);
      Serial.print(message);
      Serial.flush();
  } else if (inputString=="clon" && passive_algorithm == 0) {
      digitalWrite(LED,HIGH);
      Serial.print("City lights on");
      Serial.flush();
  } else if (inputString=="cloff" && passive_algorithm == 0) {
      digitalWrite(LED,LOW);
      Serial.print("City lights off");
      Serial.flush();
  } else if (inputString=="solar" && passive_algorithm == 0) {
      digitalWrite(led3,HIGH);
      digitalWrite(led8,LOW);
      Serial.print("solar");
      Serial.flush();
  } else if (inputString=="eolic" && passive_algorithm == 0) {
      digitalWrite(led8,HIGH);
      digitalWrite(led3,LOW);
      Serial.print("eolic");
      Serial.flush();
  } else if (inputString=="none" && passive_algorithm == 0) {
      digitalWrite(led3,LOW);
      digitalWrite(led8,LOW);
      digitalWrite(LED,LOW);
      Serial.print("none");
      Serial.flush();
  } else if (inputString=="watering" && passive_algorithm == 0) {
      tone(buzzer,3500);
      delay(400);
      noTone(buzzer);
      Serial.print("watering");
      Serial.flush();
  } else if (inputString == "passiveOff")  {
      passive_algorithm = 1;
      Serial.print("passiveOff");
      Serial.flush();
  } else if (inputString == "passiveOn") {
      passive_algorithm = 0;
      Serial.print("passiveOn");
      Serial.flush();
  } else if (inputString=="userclon") {
      digitalWrite(LED,HIGH);
      Serial.print("City lights on");
      Serial.flush();
  } else if (inputString=="usercloff") {
      digitalWrite(LED,LOW);
      Serial.print("City lights off");
      Serial.flush();
  } else if (inputString=="usersolar") {
      digitalWrite(led3,HIGH);
      digitalWrite(led8,LOW);
      Serial.print("solar");
      Serial.flush();
  } else if (inputString=="usereolic") {
      digitalWrite(led8,HIGH);
      digitalWrite(led3,LOW);
      Serial.print("eolic");
      Serial.flush();
  } else if (inputString=="usernone") {
      digitalWrite(led3,LOW);
      digitalWrite(led8,LOW);
      digitalWrite(LED,LOW);
      Serial.print("none");
      Serial.flush();
  } else if (inputString=="userwatering") {
      tone(buzzer,3500);
      delay(400);
      noTone(buzzer);
      Serial.print("watering");
      Serial.flush();
  }
  }
