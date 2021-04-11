#include <M5Stack.h>

int cnt = 0;

void setup() {
  M5.begin(); // 初期化処理
  delay(500);
  // 文字の色とサイズ
  M5.Lcd.setTextColor(WHITE);
  M5.Lcd.setTextSize(4);
}

void loop() {
  // Aボタンが押されたら+1
  if(M5.BtnA.wasPressed())
  {
    cnt++;
    M5.Lcd.clear(); // 画面全体を消去
  }

  // Bボタンが押されたら-1
  if(M5.BtnB.wasPressed())
  {
    cnt--;
    M5.Lcd.clear(); // 画面全体を消去
  }

  // Cボタンが押されたら0
  if(M5.BtnC.wasPressed())
  {
    cnt = 0;
    M5.Lcd.clear(); // 画面全体を消去
  }
  delay(30);

  M5.Lcd.drawString("CNT=" + String(cnt), 0, 40); // カウント値を表示
  M5.update();  // ボタン操作の状況を読み込む関数(ボタン操作を行う際は必須)
}
