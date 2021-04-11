#include <M5Stack.h>

float value1 = 0;
float value2 = 0;
float voltage1 = 0;
float voltage2 = 0;
const int CH1_PIN = 35;
const int CH2_PIN = 36;
const float MAX_VOLTAGE = 3.3; // 3.3Vを電源とした場合
const float ANALOG_MAX = 4095; // ESP32の場合

void setup() {
  M5.begin(); // 初期化処理
  delay(500);
  // 文字の色とサイズ
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(4);
}

void loop() {
  // CH1, CH2(35, 36pin)のアナログ入力を取得し電圧に変換
  value1 = analogRead(CH1_PIN);
  value2 = analogRead(CH2_PIN);
  voltage1 = value1 * MAX_VOLTAGE / ANALOG_MAX;
  voltage2 = value2 * MAX_VOLTAGE / ANALOG_MAX;

  
  // CH1, CH2(35, 36pin)の電圧とアナログ入力値を表示
  M5.Lcd.fillScreen(BLACK);
  M5.Lcd.setTextSize(4);
  M5.Lcd.drawString("CH1=" + String(voltage1) + "V", 0, 0);
  M5.Lcd.drawString("CH2=" + String(voltage2) + "V", 0, 40);
  M5.Lcd.setTextSize(2);
  M5.Lcd.drawString("CH1=" + String(value1) + "", 0, 80);
  M5.Lcd.drawString("CH2=" + String(value2) + "", 0, 100);
  delay(100);

}
