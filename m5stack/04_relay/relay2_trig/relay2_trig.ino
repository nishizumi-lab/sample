#include <M5Stack.h>

// 初期値
const int CH1_PIN = 35; // CH1のピン番号
const float MAX_VOLTAGE = 3.3; // 3.3Vを電源とした場合
const float ANALOG_MAX = 4095; // ESP32の場合
float value1 = 0; // CH1のアナログ値(0-4095)
float voltage1 = 0; // CH1の電圧(0-3.3V)
float realVoltage1 = 0; // CH1の真の電圧(分圧器の倍率を掛けたもの)
float trigUpper = 3; // CH1のトリガ電圧(上限)
float trigLower = -1; // CH1のトリガ電圧(下限)
float timer = 0; // リレーをONする時間(ms:0なら無限)
float alpha = 1.0; // 倍率(分圧抵抗)
String selectedItem = "trigVoltage1"; // 設定値を変更できるパラメータ
int selectedNum = 0; // 設定値を変更できるパラメータ番号
int chColor = 0x07E0;
int orgchColor = 0xFFFF;
int trigUpperColor = 0xEC42;
int trigLowerColor = 0xFFFF;
int alphaColor = 0xFFFF;
int timerColor = 0xFFFF;
int bgColor = 0x0000;
#define RELAY_PIN1 21

void setup() {
  M5.begin(); // 初期化処理

  // リレーを接続したピンを出力モードに変更
  pinMode(RELAY_PIN1, OUTPUT);
  // リレーOFF
  digitalWrite(RELAY_PIN1, LOW);
  
  delay(500);
  // 文字の色とサイズ
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(4);
}

void loop() {
  // CH1, CH2(35, 36pin)のアナログ入力を取得し電圧, 真の電圧(倍率を掛けたもの)に変換
  value1 = analogRead(CH1_PIN);
  voltage1 = value1 * MAX_VOLTAGE / ANALOG_MAX;
  realVoltage1 = alpha * voltage1;

  // CH1の電圧がトリガ電圧上限以上,もしくは下限以下の場合
  if(realVoltage1 >= trigUpper || realVoltage1 <= trigLower){
    bgColor = 0xF800; // 背景色の変更
    digitalWrite(RELAY_PIN1, HIGH); // リレー1をON
 
    // タイマーが0でなれば指定時間後にリレーOFF
    if(timer != 0){
      delay(timer);
      digitalWrite(RELAY_PIN1, LOW); // リレー1をOFF
      delay(1000);
    }
  }

  else{
     bgColor = 0x0000; // 背景色の変更
     digitalWrite(RELAY_PIN1, LOW); // リレー1をOFF
  }

  // 画面表示
  M5.Lcd.fillScreen(bgColor);
  M5.Lcd.setTextSize(4);
  M5.Lcd.setTextColor(chColor);
  M5.Lcd.drawString("CH1=" + String(realVoltage1) + "V", 20, 20);
  M5.Lcd.setTextSize(2);
  M5.Lcd.setTextColor(orgchColor);
  M5.Lcd.drawString("ORG CH1=" + String(voltage1) + "V", 0, 100);
  M5.Lcd.setTextColor(trigUpperColor);
  M5.Lcd.drawString("TRIG Upper=" + String(trigUpper) + "V", 0, 140);
  M5.Lcd.setTextColor(trigLowerColor);
  M5.Lcd.drawString("TRIG Lower=" + String(trigLower) + "V", 0, 160);
  M5.Lcd.setTextColor(alphaColor);
  M5.Lcd.drawString("Alpha=" + String(alpha) + "", 0, 180);
  M5.Lcd.setTextColor(timerColor);
  M5.Lcd.drawString("Timer=" + String(timer) + "msec", 0, 200);                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
  delay(100);

  // Aボタンが押されたら+1
  if(M5.BtnA.wasPressed() && selectedItem == "trigUpper")
  {
    trigUpper++;
  }
  if(M5.BtnA.wasPressed() && selectedItem == "trigLower")
  {
    trigLower++;
  }
    if(M5.BtnA.wasPressed() && selectedItem == "alpha")
  {
    alpha++;
  }
  if(M5.BtnA.wasPressed() && selectedItem == "timer")
  {
    timer++;
  }
  // Bボタンが押されたら-1
  if(M5.BtnB.wasPressed() && selectedItem == "trigUpper")
  {
    trigUpper--;
  }
  if(M5.BtnB.wasPressed() && selectedItem == "trigLower")
  {
    trigLower--;
  }  
  if(M5.BtnB.wasPressed() && selectedItem == "alpha")
  {
    alpha--;
  }
  if(M5.BtnB.wasPressed() && selectedItem == "timer")
  {
    timer--;
  }
  
  // Cボタンが押されたら選択アイテムを変更
  if(M5.BtnC.wasPressed())
  {
    selectedNum++; // 選択アイテム管理用の変数を加算
    
    // 選択対象をトリガ電圧下限に変更
    if(selectedNum == 1){
      selectedItem = "trigLower";
      timerColor = 0xFFFF;
      trigUpperColor = 0xFFFF;
      trigLowerColor = 0xEC42;
      alphaColor = 0xFFFF;         
    }
    // 選択対象を分圧抵抗の倍率に変更
    else if(selectedNum == 2){
      selectedItem = "alpha";
      timerColor = 0xFFFF;
      trigUpperColor = 0xFFFF;
      trigLowerColor = 0xFFFF;
      alphaColor = 0xEC42;  
    }
    // 選択対象をトリガ電圧上限に変更
    else if(selectedNum == 3){
      selectedItem = "timer";
      timerColor = 0xEC42;
      trigUpperColor = 0xFFFF;
      trigLowerColor = 0xFFFF;
      alphaColor = 0xFFFF;   
    }
    else{
      selectedNum = 0;
      selectedItem = "trigUpper";
      trigUpperColor = 0xEC42;
      trigLowerColor = 0xFFFF;
      alphaColor = 0xFFFF;   
    }
  }
    M5.update();  // ボタン操作の状況を読み込む関数(ボタン操作を行う際は必須)
}
