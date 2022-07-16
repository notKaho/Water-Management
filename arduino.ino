#include "DHT.h"
#define DHTPIN A5
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Avoid
int isObstaclePin = 2;  // This is our input pin
int isObstacle = HIGH;  // HIGH MEANS NO OBSTACLE
//RGB
int redpin = 11;
int greenpin = 10;
int bluepin = 9;
//LDR
int sensorPin = A2;
int sensorValue = 0;

void setup() {
  //Avoid
  pinMode(isObstaclePin, INPUT);
  Serial.begin(9600);
  //RGB
  pinMode(redpin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  pinMode(bluepin, OUTPUT);
  dht.begin();
}

void loop()
{
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t))
  {
    return;
  }
  
  //Avoid
  isObstacle = digitalRead(isObstaclePin);

  //LDR
  sensorValue = analogRead(sensorPin);

  if (sensorValue > 300)
  {
    Serial.print(String(isObstacle));
    Serial.print(",");
    Serial.print(String(sensorValue));
    Serial.print(",");
    Serial.print(t);
    Serial.print(",");
    Serial.print(h);
    Serial.print(",");
    Serial.println("1");
    delay(1500);
    analogWrite(11, 255);
    analogWrite(10, 255);
    analogWrite(9, 255);
  }
  else
  {
    Serial.print(String(isObstacle));
    Serial.print(",");
    Serial.print(String(sensorValue));
    Serial.print(",");
    Serial.print(t);
    Serial.print(",");
    Serial.print(h);
    Serial.print(",");
    Serial.println("0");
    delay(1500);
    analogWrite(11, 0);
    analogWrite(10, 0);
    analogWrite(9, 0);
  }
}
