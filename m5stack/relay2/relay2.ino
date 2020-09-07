/*
    Description: Use RELAY to switch on and off the circuit.
*/
#include <M5Stack.h>

void setup() {
  M5.begin();
  M5.Power.begin();
  M5.Lcd.clear(BLACK);
  M5.Lcd.setTextFont(5);
  M5.Lcd.setTextColor(GREEN, BLACK);
  M5.Lcd.setCursor(50, 0, 4);
  //disable the speak noise
  dacWrite(22, 0);
  pinMode(21, OUTPUT);
}

int onTime = 50;

void loop(void) {
    M5.update();
   M5.Lcd.setCursor(0, 0); // カーソル
    M5.Lcd.setTextColor(GREEN, BLACK);  // 色
    M5.Lcd.printf("ON TIME[ms]: %d",onTime);
    digitalWrite(21, LOW);
    // Aボタン
    if (M5.BtnA.wasPressed()) {
      M5.Lcd.setCursor(50,150);
      M5.Lcd.printf("later 20sec ON");
      delay(5000);
      M5.Lcd.setTextFont(5);
      M5.Lcd.setTextColor(WHITE, RED);
      M5.Lcd.printf("done");
      M5.Lcd.clear(RED);
      digitalWrite(21, HIGH);
      delay(onTime);
      M5.Lcd.clear(BLACK);
      M5.update();
     // M5.Lcd.printf("ON TIME[ms]: %d",onTime);
    }
    // Bボタン
    if (M5.BtnB.wasPressed()) {
      // カウンタ更新
      onTime++;
      // カウンタ表示
    }
    // Cボタン
    if (M5.BtnC.wasPressed()) {
      onTime--;
    }
}
