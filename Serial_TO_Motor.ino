#include <Servo.h>
byte motorPin = 9;  // Pin connected to the ESC or motor

Servo servo;

void setup() {
    Serial.begin(9600);  // Start serial communication at 9600 baud rate
    servo.attach(motorPin);

    Serial.println("Setup..");
    servo.writeMicroseconds(1500);
    //Let the esc recognize the "stop"-signal
    delay(7000);
}

void loop() {
    if (Serial.available() > 0) {
        // Read the incoming serial data
        String data = Serial.readStringUntil('\n');
        int motorSpeed = data.toInt();  // Convert the string to an integer

        // Constrain the motor speed to be within valid range (0-255)
        motorSpeed = constrain(motorSpeed, 1100, 1900);

        // Write the PWM signal to control the motor
        servo.writeMicroseconds(motorSpeed);

        // For debugging, print the motor speed
        Serial.print("Motor Speed: ");
        Serial.println(motorSpeed);
    }
}
