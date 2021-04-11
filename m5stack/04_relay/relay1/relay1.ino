#include <M5Stack.h>

#define RELAY_PIN1 21
#define RELAY_PIN2 22

void setup() {
  M5.begin();
  // リレーを接続したピンを出力モードに変更
  pinMode(RELAY_PIN1, OUTPUT);
  pinMode(RELAY_PIN2, OUTPUT);
  // リレーOFF
  digitalWrite(RELAY_PIN1, LOW);
  digitalWrite(RELAY_PIN2, LOW);
}

void loop() {
  // Aボタンを押したらリレー1をON
  if(M5.BtnA.wasPressed()){
    digitalWrite(RELAY_PIN1, HIGH);
  }
  // Bボタンを押したらリレー2をON
  if(M5.BtnB.wasPressed()){
    digitalWrite(RELAY_PIN2, HIGH);
  }
    // Bボタンを押したらリレー2をON(1000ms)
  if(M5.BtnC.wasPressed()){
    digitalWrite(RELAY_PIN1, LOW);
    digitalWrite(RELAY_PIN2, LOW);
  }
  delay(30);
  M5.update(); // ボタン操作の取得に必要
}
