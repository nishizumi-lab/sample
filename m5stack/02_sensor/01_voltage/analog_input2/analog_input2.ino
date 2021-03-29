#include <M5Stack.h>

const int CH1_PIN = 35;
const int CH2_PIN = 36;
const float MAX_VOLTAGE = 3.3; // 3.3Vを電源とした場合
const float ANALOG_MAX = 4095; // ESP32の場合
float value1 = 0;
float value2 = 0;
float voltage1 = 0;
float voltage2 = 0;
float realVoltage1 = 0;
float realVoltage2 = 0;
float trigVoltage1 = 3;
float trigVoltage2 = 3;
float alpha = 1.0; // 倍率(分圧抵抗)
String selectedItem = "trigVoltage1";
int selectedNum = 0;

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
  realVoltage1 = alpha * voltage1;
  realVoltage2 = alpha * voltage2;
  

  M5.Lcd.fillScreen(BLACK);

  if(realVoltage1 >= trigVoltage1){
    M5.Lcd.fillScreen(RED);
  }
  else if(realVoltage2 >= trigVoltage2){
    M5.Lcd.fillScreen(ORANGE);
  }
  // CH1, CH2(35, 36pin)の電圧とアナログ入力値を表示
  M5.Lcd.setTextSize(4);
  M5.Lcd.drawString("CH1=" + String(realVoltage1) + "V", 0, 0);
  M5.Lcd.drawString("CH2=" + String(realVoltage2) + "V", 0, 40);
  M5.Lcd.setTextSize(2);
  M5.Lcd.drawString("ORG CH1=" + String(voltage1) + "V", 0, 100);
  M5.Lcd.drawString("ORG CH2=" + String(voltage2) + "V", 0, 120);
  M5.Lcd.drawString("TRIG CH1=" + String(trigVoltage1) + "V", 0, 140);
  M5.Lcd.drawString("TRIG CH2=" + String(trigVoltage2) + "V", 0, 160);
  M5.Lcd.drawString("alpha=" + String(alpha) + "", 0, 180);
  M5.Lcd.drawString("select> " + selectedItem, 0, 220);
  delay(100);

  // Aボタンが押されたら+1
  if(M5.BtnA.wasPressed() && selectedItem == "trigVoltage1")
  {
    trigVoltage1++;
  }
  if(M5.BtnA.wasPressed() && selectedItem == "trigVoltage2")
  {
    trigVoltage2++;
  }
    if(M5.BtnA.wasPressed() && selectedItem == "alpha")
  {
    alpha++;
  }
  
  // Bボタンが押されたら-1
  if(M5.BtnB.wasPressed() && selectedItem == "trigVoltage1")
  {
    trigVoltage1--;
  }
  if(M5.BtnB.wasPressed() && selectedItem == "trigVoltage2")
  {
    trigVoltage2--;
  }  
  if(M5.BtnB.wasPressed() && selectedItem == "alpha")
  {
    alpha--;
  }
  
  // Cボタンが押されたら選択アイテムを変更
  if(M5.BtnC.wasPressed())
  {
    selectedNum++; // 選択アイテム管理用の変数を加算
    if(selectedNum == 1){
      selectedItem = "trigVoltage2";         
    }
    else if(selectedNum == 2){
      selectedItem = "alpha";         
    }
    else{
      selectedNum = 0;
      selectedItem = "trigVoltage1";    
    }
  }
    M5.update();  // ボタン操作の状況を読み込む関数(ボタン操作を行う際は必須)
}
