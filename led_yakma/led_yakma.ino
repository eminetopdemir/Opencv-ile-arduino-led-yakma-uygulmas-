 int led1 = 7;  // Birinci LED
 int led2 = 8;  // İkinci LED

void setup() {
  pinMode(led1, OUTPUT);
  pinMode(led2, OUTPUT);
  Serial.begin(9600);  // Seri iletişimi başlat
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();

    if (command == '0') {
      digitalWrite(led1, LOW);
      digitalWrite(led2, LOW);
    }
    else if (command == '1') {
      digitalWrite(led1, HIGH);
      digitalWrite(led2, LOW);
    }
    else if (command == '2') {
      digitalWrite(led1, LOW);
      digitalWrite(led2, HIGH);
    }
    else if (command == '3') {
      digitalWrite(led1, HIGH);
      digitalWrite(led2, HIGH);
    }
  }
}
