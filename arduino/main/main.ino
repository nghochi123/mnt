#include <Stepper.h>
#include <Servo.h>

// Definitions
#define NEMASPR 200 // NEMA Steps per revolution
// NEMA Stepper Ports, n to n + 3
#define S1PORT 1
#define S2PORT 9
#define S3PORT 16

// Initialize stepper mototrs and position of stepper motors
Stepper stepper1(NEMASPR, S1PORT, S1PORT + 1, S1PORT + 2, S1PORT + 3);
Stepper stepper2(NEMASPR, S2PORT, S2PORT + 1, S2PORT + 2, S2PORT + 3);
Stepper stepper3(NEMASPR, S3PORT, S3PORT + 1, S3PORT + 2, S3PORT + 3);

int s1 = 0;
int s2 = 0;
int s3 = 0;

// Input from bluetooth
String readString;
char c;
char c2 = '0';
int choice;

void setup()
{
    // Board serial
    Serial.begin(9600);
    Serial.println("Serial started at 9600");

    // Bluetooth serial (TX3 RX3)
    Serial3.begin(9600);
    Serial3.println("HC-06 started at 9600");

    pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
    if (Serial3.available() > 0) // Connected to Bluetooth
    {
        c = Serial3.read();
        readString += c;
        choice = readString.toInt();

        // Input from bluetooth - choice.
        switch (choice)
        {
        case 1:
            digitalWrite(LED_BUILTIN, HIGH);
            Serial.write("You have inputted 1\n");
            adjust(c2);
            break;
        case 2:
            digitalWrite(LED_BUILTIN, LOW);
            Serial.write("You have inputted 2\n");
            adjust(c2);
            break;
        case 3:
            digitalWrite(LED_BUILTIN, HIGH);
            Serial.write("You have inputted 3\n");
            adjust(c2);
            break;
        default:
            Serial.write("Invalid - only 1 2 or 3 allowed\n");
        }
    }
    readString = "";
    c2 = '0';
}

void adjust(char c2)
{
    while (c2 != 'q')
    {
        if (Serial3.available() > 0) // Connected to Bluetooth
        {
            c2 = Serial3.read();
            switch (c2 - '0')
            {
            case 1:
                digitalWrite(LED_BUILTIN, HIGH);
                break;
            case 2:
                digitalWrite(LED_BUILTIN, LOW);
                break;
            default:
                Serial.write("S");
            }
        }
    }
    Serial.write("Exiting while loop");
}