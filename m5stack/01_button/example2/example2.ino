#include <M5Stack.h>

int v1 = 0;
int v2 = 0;
int v3 = 0;
String selectedItem = "V1";
int selectedNum = 0;

void setup() {
  M5.begin(); // 初期化処理
  delay(500);
  // 文字の色とサイズ
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(4);
}

void loop() {
  // Aボタンが押されたら+1
  if(M5.BtnA.wasPressed() && selectedItem == "V1")
  {
    v1++;
    M5.Lcd.clear(); // 画面全体を消去
  }
  if(M5.BtnA.wasPressed() && selectedItem == "V2")
  {
    v2++;
    M5.Lcd.clear(); // 画面全体を消去
  }
    if(M5.BtnA.wasPressed() && selectedItem == "V3")
  {
    v3++;
    M5.Lcd.clear(); // 画面全体を消去
  }
  
  // Bボタンが押されたら-1
  if(M5.BtnB.wasPressed() && selectedItem == "V1")
  {
    v1--;
    M5.Lcd.clear(); // 画面全体を消去
  }
  if(M5.BtnB.wasPressed() && selectedItem == "V2")
  {
    v2--;
    M5.Lcd.clear(); // 画面全体を消去
  }  if(M5.BtnB.wasPressed() && selectedItem == "V3")
  {
    v3--;
    M5.Lcd.clear(); // 画面全体を消去
  }
  
  // Cボタンが押されたら選択アイテムを変更
  if(M5.BtnC.wasPressed())
  {
    selectedNum++; // 選択アイテム管理用の変数を加算
    if(selectedNum == 1){
      selectedItem = "V2";         
    }
    else if(selectedNum == 2){
      selectedItem = "V3";         
    }
    else{
      selectedNum = 0;
      selectedItem = "V1";    
    }
    M5.Lcd.clear(); // 画面全体を消去
  }
  delay(30);

  M5.Lcd.drawString("V1=" + String(v1), 0, 0); // カウント値を表示
  M5.Lcd.drawString("V2=" + String(v2), 0, 40); // カウント値を表示
  M5.Lcd.drawString("V3=" + String(v3), 0, 80); // カウント値を表示
  M5.Lcd.drawString("selected>" + selectedItem, 0, 120); // カウント値を表示
  M5.update();  // ボタン操作の状況を読み込む関数(ボタン操作を行う際は必須)
}
