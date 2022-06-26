char c;

//D18 is A4
//D19 is A5
String readString;

void setup()
{
  Serial.begin(9600);
  Serial.println("Serial started at 9600");

  Serial3.begin(9600);
  Serial.println("BTserial started at 9600");
}

void loop()
{

  if (Serial.available() > 0)
  {
    c = Serial.read();
    readString += c;
    readString.trim();
    if (readString == "s") {
      Serial3.write("PENIS");
    }
    Serial3.write(c);
    Serial.write(c);
  }


  if (Serial3.available() > 0)
  {
    c = Serial3.read();
    Serial.write(c);
  }
  readString = "";
}
