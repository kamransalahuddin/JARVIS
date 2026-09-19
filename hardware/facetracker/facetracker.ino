#include <Servo.h>

String inputString;

Servo left_right;
Servo up_down;
int x = 90;
int y = 90;
void setup()
{
  left_right.attach(9);
  up_down.attach(7);
  Serial.begin(115200);

  
}

void loop()
{
  while(Serial.available()>0)
  {
    inputString = Serial.readStringUntil('\r');
    Serial.println(inputString);

    int x_axis = inputString.substring(0, inputString.indexOf(',')).toInt();
    int y_axis = inputString.substring(inputString.indexOf(',') + 1).toInt();

    y += y_axis / 60;
    y = constrain(y, 0, 180);

    x += x_axis / 60;
    x = constrain(x, 0, 180);

    left_right.write(x);
    up_down.write(y);

    // Print the parsed values
    Serial.print("First Integer: ");
    Serial.println(x);
    Serial.print("Second Integer: ");
    Serial.println(y);
  }
}