String lane;

int signal1[] = {22, 24, 26}; //{Red, Yellow, Green}
int signal2[] = {46, 48, 50}; //{Red, Yellow, Green}
int signal3[] = {13, 12, 11}; //{Red, Yellow, Green}
int signal4[] = {10, 9, 8}; //{Red, Yellow, Green}

int redDelay = 5000;
int yellowDelay = 2000;

void setup(){
  Serial.begin(9600);

  for (int i = 0; i < 3; i++) {
      pinMode(signal1[i], OUTPUT);
      pinMode(signal2[i], OUTPUT);
      pinMode(signal3[i], OUTPUT);
      pinMode(signal4[i], OUTPUT);
   }
}

void loop(){
    if (Serial.available() > 0) {
      lane=Serial.readStringUntil('\r');
      executeInstruction(lane);
    }
  }
  void executeInstruction(String lane){
    
    if (lane == "1") {
      // Making Green LED at signal 1 and red LEDs at other signals HIGH
      digitalWrite(signal1[2], HIGH);
      digitalWrite(signal1[0], LOW);
      digitalWrite(signal2[0], HIGH);
      digitalWrite(signal3[0], HIGH);
      digitalWrite(signal4[0], HIGH);
      delay(redDelay);

      // Making Green LED at signal 1 LOW and making yellow LED at signal 1 blink twice
      for (int i = 0; i < 2; i++) {
        digitalWrite(signal1[1], HIGH);
        digitalWrite(signal1[2], LOW);
        delay(500);
        digitalWrite(signal1[1], LOW);
        delay(500);
      }
      digitalWrite(signal1[1], LOW); // Ensure the yellow LED is off after blinking

    } else if (lane == "2") {
      // Making Green LED at signal 2 and red LEDs at other signals HIGH
      digitalWrite(signal1[0], HIGH);
      digitalWrite(signal2[2], HIGH);
      digitalWrite(signal2[0], LOW);
      digitalWrite(signal3[0], HIGH);
      digitalWrite(signal4[0], HIGH);
      delay(redDelay);

      // Making Green LED at signal 2 LOW and making yellow LED at signal 2 blink twice
      for (int i = 0; i < 2; i++) {
        digitalWrite(signal2[1], HIGH);
        digitalWrite(signal2[2], LOW);
        delay(500);
        digitalWrite(signal2[1], LOW);
        delay(500);
      }
      digitalWrite(signal2[1], LOW); // Ensure the yellow LED is off after blinking

    } else if (lane == "3") {
      // Making Green LED at signal 3 and red LEDs at other signals HIGH
      digitalWrite(signal1[0], HIGH);
      digitalWrite(signal2[0], HIGH);
      digitalWrite(signal3[2], HIGH);
      digitalWrite(signal3[0], LOW);
      digitalWrite(signal4[0], HIGH);
      delay(redDelay);

      // Making Green LED at signal 3 LOW and making yellow LED at signal 3 blink twice
      for (int i = 0; i < 2; i++) {
        digitalWrite(signal3[1], HIGH);
        digitalWrite(signal3[2], LOW);
        delay(500);
        digitalWrite(signal3[1], LOW);
        delay(500);
      }
      digitalWrite(signal3[1], LOW); // Ensure the yellow LED is off after blinking

    } else if (lane == "4") {
        // Making Green LED at signal 4 and red LEDs at other signals HIGH
        digitalWrite(signal1[0], HIGH);
        digitalWrite(signal2[0], HIGH);
        digitalWrite(signal3[0], HIGH);
        digitalWrite(signal4[2], HIGH);
        digitalWrite(signal4[0], LOW);
        delay(redDelay);

        // Making Green LED at signal 4 LOW and making yellow LED at signal 4 blink twice
        for (int i = 0; i < 2; i++) {
          digitalWrite(signal4[1], HIGH);
          digitalWrite(signal4[2], LOW);
          delay(500);
          digitalWrite(signal4[1], LOW);
          delay(500);
        }
        digitalWrite(signal4[1], LOW);
    } else {
      // Invalid lane
      Serial.println("Invalid lane number. Please enter 1, 2, 3, or 4.");
    }
  }
