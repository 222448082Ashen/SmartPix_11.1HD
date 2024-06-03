#include <dht11.h>
#define DHT11PIN 8

const int trigPin = 14;
const int echoPin = 15;
const int pirPin = 2;
const int buzzerPin = 16;
const int ledPin = 1;
const int ldrPin = A0;
const int mq2Pin = A1;

dht11 DHT11;

bool buzzerEnabled = true;

void setup() {
  Serial.begin(9600);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(pirPin, INPUT);
  pinMode(buzzerPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(ldrPin, INPUT);
  pinMode(mq2Pin, INPUT);

  Serial.println("System Initialized");
}

void loop() {
  Serial.println("----- Sensor Readings -----");

  // DHT11 Sensor
  int chk = DHT11.read(DHT11PIN);
  float humidity = DHT11.humidity;
  float temperature = DHT11.temperature;
  Serial.print("Humidity (%): ");
  Serial.println(humidity, 2);
  Serial.print("Temperature (C): ");
  Serial.println(temperature, 2);

  // Ultrasonic Sensor
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = (duration / 2) / 29.1;
  Serial.print("Distance (cm): ");
  Serial.println(distance);

  // PIR Sensor
  int pirStatus = digitalRead(pirPin);
  Serial.print("PIR Status: ");
  Serial.println(pirStatus);

  // MQ2 Gas Sensor
  int mq2Status = analogRead(mq2Pin);
  Serial.print("MQ2 Gas Level: ");
  Serial.println(mq2Status);

  // LDR Sensor
  int ldrStatus = analogRead(ldrPin);
  int pwmValue = map(ldrStatus, 0, 1023, 255, 0);
  analogWrite(ledPin, pwmValue);
  Serial.print("LDR Status: ");
  Serial.print(ldrStatus);
  Serial.print(" - LED Brightness: ");
  Serial.println(pwmValue);

  // Control buzzer based on multiple conditions
  if ((pirStatus == HIGH || distance <=4 || mq2Status > 3000 || temperature >= 30 || temperature <= 10) && buzzerEnabled) {
    tone(buzzerPin, 1000); // Play a 1000Hz tone
  } else {
    noTone(buzzerPin); // Stop the tone
  }

  // Check for commands from Python
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "stopBuzzer") {
      buzzerEnabled = false;
      noTone(buzzerPin); // Ensure the buzzer is stopped
      Serial.println("Buzzer stopped");
    } else if (command == "startBuzzer") {
      buzzerEnabled = true;
      Serial.println("Buzzer enabled");
    }
  }

  delay(2000);
}
